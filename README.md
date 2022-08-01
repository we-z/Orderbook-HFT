# orderbook-hft
Order Book Imbalance trading strategy

## deployment on GCP Debian

```
apt-get upgrade
timedatectl set-timezone America/New_York
git clone https://github.com/we-z/orderbook-hft.git
apt install python3-pip
cd orderbook-hft
pip3 install -r requirements.txt
```

## cron
```
crontab -e

30 9 * * 1-5 screen -S minute-trader -X stuff "sudo python3 /home/path/to/orderbook-hft/main.py^M"

55 15 * * 1-5 screen -S minute-trader -X stuff "^C"
55 15 * * 1-5 screen -S minute-trader -X stuff "^C"
56 15 * * 1-5 screen -S minute-trader -X stuff "sudo python3 /home/path/to/orderbook-hft/liquidate.py^M"
```
