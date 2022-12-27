# Itarate over all text files insite training_data folder
# and compress them into a single file

import glob
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Get all text files inside training_data folder
files = glob.glob("training_data/*.txt")
response_user = os.getenv("RESPONSE_USER")
messages_per_conversation = 1000
whatsapp_welcome_message = "As mensagens e as chamadas são protegidas"


def remove_escape_chars(line):
    line = line.replace('"', "'")
    line = line.replace("\\", "")
    return line.replace("\n", " ")


def get_message(text):
    # Trim the text
    splited = text.split(":")
    if len(splited) == 2:
        return str(text.split(":")[1]).strip()
    else:
        return ""


def get_user(text):
    return str(text.split(":")[0]).strip()


def parse_message(line):
    line_without_date = remove_escape_chars(line[19:])
    line_date = line[:16]
    try:
        if "<Arquivo de mídia oculto>" in line_without_date:
            return None
        return {
            "user": get_user(line_without_date),
            "message": get_message(line_without_date),
            "date_time": datetime.strptime(line_date, "%d/%m/%Y %H:%M"),
        }
    except:
        return None


def get_next_line(lines, next_line_i):

    if next_line_i >= len(lines) or next_line_i + 1 >= len(lines):
        return next_line_i, "break"

    # If the current line does not have :, skip it
    if ":" not in lines[next_line_i]:
        return next_line_i + 1, None

    # Next line needs to have ":"
    if ":" not in lines[next_line_i + 1]:
        current_line = parse_message(lines[next_line_i])
        next_line_i += 1
        if current_line is None:
            return next_line_i + 1, None
        # Append same date and user as last message
        return next_line_i, {
            "user": current_line["user"],
            "message": remove_escape_chars(lines[next_line_i]),
            "date_time": current_line["date_time"],
        }

    next_line_i += 1
    return next_line_i, parse_message(lines[next_line_i])


# Open a file to write compressed data
with open("training_data.jsonl", "w+") as fout:
    # Iterate over all files
    for filename in files:
        # Open file for reading
        with open(filename, "r") as fin:
            # Read all lines
            lines = fin.readlines()[-messages_per_conversation:]
            i = 0
            response_count = 0
            conversations = []
            while i <= len(lines):
                if i >= len(lines):
                    break
                line_data = remove_escape_chars(lines[i][19:])
                if line_data.startswith(whatsapp_welcome_message):
                    i += 1
                    continue

                conversation = []
                current = parse_message(lines[i])
                if current is not None:
                    conversation.append(current)

                next_line = None

                while next_line is None:
                    i, next_line = get_next_line(lines, i)

                if next_line == "break" or len(conversation) == 0:
                    break

                # Append all messaes until the next message
                # has more than 1 hour of difference
                while (
                    next_line["date_time"] - conversation[-1]["date_time"]
                ).total_seconds() < 3600:
                    conversation.append(next_line)
                    i, next_line = get_next_line(lines, i)
                    while next_line is None or next_line == "break":
                        i, next_line = get_next_line(lines, i)
                        if next_line == "break":
                            break
                    if next_line == "break":
                        break

                conversations.append(conversation)

            # Get all conversations without the last message
            for conversation in conversations:
                promps = []
                compls = []

                # Append last responses into compls
                it = len(conversation) - 1
                while it >= 0 and conversation[it]["user"] != response_user:
                    it -= 1

                while it >= 0 and conversation[it]["user"] == response_user:
                    compls.append(conversation[it])
                    it -= 1

                # Append all messages before the last response into promps
                while it >= 0:
                    promps.append(conversation[it])
                    it -= 1

                # Reverse the lists
                promps.reverse()
                compls.reverse()

                # Create prompt and completion strings
                prompt = ""
                completion = ""
                for promp in promps:
                    prompt += promp["user"] + ": " + promp["message"] + "\\n"
                prompt += response_user + ": "

                if len(compls) == 0 or len(promps) == 0:
                    continue

                completion = compls[0]["message"] + "\\n"
                for compl in compls[1:]:
                    completion += compl["user"] + ": " + compl["message"] + "\\n"

                # Write the prompt and completion to the file
                fout.write(
                    '{"prompt":"' + prompt + '", "completion":"' + completion + '"}\n'
                )

            message_count = sum([len(conversation) for conversation in conversations])
            not_response_user = ""
            # Get the last user from conversation message which arent the response user
            for conv in conversations:
                for promp in conv:
                    if promp["user"] != response_user:
                        not_response_user = promp["user"]
                        break
                if not_response_user != "":
                    break
            print(f"{message_count} messages processed for user {not_response_user}")
