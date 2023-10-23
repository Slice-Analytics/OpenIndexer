Setup instructions:
- Start by cloning the repo
- Create virtual environment
- PIP install required packages
    CMD: pip install python-dotenv web3 supabase telebot
- Determine node provider:
    Connect to a personal node
        - add example
    Common Third Party Node Providers
    Base:
    - https://getblock.io/
    Optimisim: 
    - https://www.quicknode.com/
    Note: The chosen node provider must accomodate web3 filter class (https://web3py.readthedocs.io/en/stable/filters.html) 
- Determine database 
    - Supabase, sqlite3, etc
    This example uses Supabase as it is easy to use and quick to setup

- Create .env file and generate key value pairs

- TODO: details how to get a Contract ABI: .json or etherscan
- TODO: how to setup telegram bot for easy notifications


Additional Information:

New Linux VM Instance Setup Procedure:
- Download Miniconda CMD: wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
- Install miniconda CMD: bash Miniconda3-latest-Linux-x86_64.sh
- Close and open shell to complete python installation
- Upload python  to VM Instance
- Pip install required items
- Upload service to correct file location
- CMD: sudo systemctl daemon-reload
- CMD: sudo systemctl start [service-name]

Useful Linux Terminal CMD's
- cat nohup.out  ->  Shows the print statements in the terminal
- nohup python app.py > output.txt  ->  This stores print statements in the file output.txt
- pgrep -a ping  ->  Shows the running processes and their job id's
- kill [job id]  ->  Will shut down the nohup background job
- pgrep -lf python

Creating & Starting a Service
- Create service-name.service file
- Move .service file to /etc/systemd/system
    touch [file-name]
    sudo mv [file-name] [folder-location]
- CMD: sudo systemctl daemon-reload
- CMD: sudo systemctl start [service-name]
- CMD: sudo systemctl status [service-name]

Stop a Service
- CMD: sudo systemctl stop [service-name]

Enable Service on System Boot
- CMD: sudo systemctl enable [service-name]



