sudo chmod +x ./main.py
nohup python -u ./main.py > output.log 2>&1 &
tail -f nohup.out
