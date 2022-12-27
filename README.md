# gpt-3-whatsapp-training

A project that implements GPT-3 training with whatsapp messages.

<img src="https://pbs.twimg.com/media/Fk9BfSbXgAAWRhA?format=jpg&name=large">

### How it works?

This simple Python script gets your Whatsapp conversations exported as TXT and compress into a single jsonl file which is used to train a fine-tuned Open AI GPT-3 model, to simulate your responses.

### Requirements

- OpenAI account and OpenAI API Token
- Python 3.11
- Few whatsapp conversations (More than 2000 messages)
- Around $20 to train and use the fined-tuned model

### Usage

- Create [OpenAI API](https://openai.com/api/) account
- Get the [API Key](https://beta.openai.com/account/api-keys)
- Download and install [Python 3.11](https://www.python.org/downloads/)
- Clone this repo `git clone https://github.com/felps-dev/gpt-3-whatsapp-training`
- Create a virtualenv inside the cloned repo `python3 -m venv env`
- Activate your virtual env `env/Scripts/Activate`(for windows) and `source env/bin/activate` for unix based OS (Mac, Linux, etc)
- Install requirements `pip install -r requirements.txt`
- Export your Whatsapp messages
  - Go to a conversation
  - Press 3 dots on top right corner
  - Export conversation
  - Export without media
  - Get the TXT file from each conversation
- Put the TXT files from previous step inside `training_data` folder
- Create a copy of the file `.env_template` named as `.env`
- Fill the `.env` with your info
  - RESPONSE_USER - Is your nickname on TXT files
  - OPENAI_API_KEY - Is the api key from previous steps
  - MODEL_ENGINE - Is the model generated after training finishes
- Don't worry to not have MODEL_ENGINE, you didnt made the training yet.
- Prepare the data for training using `python3 compress_training_data.py`
- This will create a new file named `training_data.jsonl`
- Start the training using the command `openai api fine_tunes.create -t training_data.jsonl -m davinci`
- You can use other models instead **davinci**, [see there](https://beta.openai.com/docs/models/gpt-3)
- Wait until the training finishes, you can get the info using `openai api fine_tunes.get -i your_ft_id_given_by_previous_command`
- Once the training finishes, you can get your model using the **info** from previous step, on `fine_tuned_model` property.
- Now put your model-id inside `MODEL_ENGINE` at **.env** file
- Start chat by using `python3 chat.py`
