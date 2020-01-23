# Install local dependencies
pip3 install -r requirements.txt
# Pull the GPT-2 submodule if it hasn't been pulled yet
git submodule update --init

cd writersblock/ai/gpt-2

# Install GPT-2 dependencies
pip3 install -r requirements.txt
# Download the GPT-2 model (~500MB)
python3 download_model.py 117M

cd ../../..

# Run the GPT-2 listening process
python3 -m writersblock.ai.main