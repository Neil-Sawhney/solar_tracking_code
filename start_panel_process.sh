git pull
sudo chmod +x ./main.py

# Check if main.py is already running
if ! pgrep -f "python -u ./main.py" > /dev/null
then
    nohup python -u ./main.py > output.log 2>&1 &
fi

tail -f output.log
