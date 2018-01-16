# Bitcoin Wallet Generator

Generates new Bitcoin wallets individually or in batch with Electrum (BIP32-compliant) standard and outputs mnemonic seed, receiving address, and corresponding QR code to image files for overlay printing on paper wallets.

<b>Install:</b>
1. Install dependencies: pip install -r requirements.txt

<b>Use:</b>
1. In home directory, run "bash create_wallets.sh n" where n is an integer number of wallets that you would like to generate.
2. Files will appear in the "wallets/" directory, filed individually by date/time of creation.

<b>Program Flow:</b>
1. Use Electrum to generate new wallet (Shell)
2. Read wallet file and parse json for seed and first receiving address, also saving to individual text files (Python)
3. Create QR code for receiving address and save to svg file, then convert to png, saving as copy (Python)
4. Write seed to svg file, formatting text for square output (Python)
5. Create canvas and place features in arrangement for printing on paper wallet (Python)
6. Save to transparent overlay file (Python)
