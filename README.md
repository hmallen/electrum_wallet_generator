# Bitcoin Wallet Generator

PUBLIC ADDRESS AND ASSOCIATED QR NOT READY FOR LIVE USE. FIX IN PROGRESS.

Generates new Bitcoin wallets individually or in batch with BIP32 standard and entropy generated from mnemonic seed.

<b>Program Flow:</b>
1. Use electrum to generate random mnemonic seed
2. Hash seed using SHA256
3. Use pybitcointools (bitcoin library) to convert hash to public hash, private hash, public address, and private address, saving everything to csv file
4. Create QR codes for public address and private key and save to svg files

<b>Options:</b>

-n/--number: Number of wallets to generate

-o/--output: Specify output csv file path

-q/--qr: Enable output of svg QR codes
