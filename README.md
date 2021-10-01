# NetBox Lab

Testing NetBox API.


## Requirements

Install required Python packages with:

    $ pip install -r requirements.txt

## Usage

1. Clone repository:

    $ git clone https://github.com/joaomcoliveira/netbox-lab

2. Change directory to netbox-lab:

    $ cd netbox-lab

3. Create a Python virtual environment:

    $ python3 -m venv ~/netbox-lab

4. Activate the virtual environment:

    $ source ~/netbox-lab/bin/activate

5. Install required Python packages via pip:

    $ pip install -r requirements.txt

6. Create and populate an .env file with NetBox URL and token:

    NB_URL=http://urlexample:8000
    NB_TOKEN=tokenexample0123456789

7. Execute Python file:

    $ python3 runbook.py

