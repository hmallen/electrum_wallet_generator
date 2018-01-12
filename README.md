# Bitcoin Wallet Generator

Generates new Bitcoin wallets individually or in batch with BIP32 standard and entropy generated from mnemonic seed.

<b>Program Flow:</b>
1. Use Electrum to generate new wallet (Shell)
2. Read wallet file and parse json (Python)
3. Save wallet seed and first receiving address to individual txt files (Python)
4. Create QR code for receiving address and save to svg file (Python)
5. Convert svg to png file, saving as copy (Python)

<b>Options:</b>

-n/--number: Number of wallets to generate

-o/--output: Specify output csv file path

-q/--qr: Enable output of svg QR codes
