# The record nobody wrote

CLAM (Clamcoin, 2014) has no wallet tooling in 2026 for one small reason.
The 2014-era libraries that generated tooling for every other chain worked
from a one-page parameter record per coin, and nobody ever wrote CLAM's.

This repository is that record:

- `registry_record.py`: per-chain parameter records for CLAM, DOGE and
  Solana in one table. It covers address/WIF/script versions, network magic,
  default P2P port, SLIP-44 coin type, and CLAM's serialization quirks (the
  nTime field and the ClamSpeech string that make its transactions unlike
  Bitcoin's). Every field carries its verification state.
- `test_vectors.json`: the public BIP-39 / SLIP-0010 vectors a correct
  implementation must reproduce. They are published test values, never real wallets.

## CLAM citation table (checked Oct 22, 2026)

Primary source: `src/chainparams.cpp` in the CLAM client,
[nochowderforyou/clams](https://github.com/nochowderforyou/clams), mainnet params.

| Parameter | Record value | Source value | Source |
|---|---|---|---|
| P2PKH version | 0x89 | 137 (0x89) | [2.1.0 @ d9ba48a L135](https://github.com/nochowderforyou/clams/blob/d9ba48af9612a7c4af802613797ce928fd6993f8/src/chainparams.cpp#L135), [master @ ac5c8cc L93](https://github.com/nochowderforyou/clams/blob/ac5c8cc04661eb181cda8651e931fcda3ad11a00/src/chainparams.cpp#L93) |
| P2SH version | 0x0d | 13 (0x0d) | [2.1.0 L136](https://github.com/nochowderforyou/clams/blob/d9ba48af9612a7c4af802613797ce928fd6993f8/src/chainparams.cpp#L136), [master L94](https://github.com/nochowderforyou/clams/blob/ac5c8cc04661eb181cda8651e931fcda3ad11a00/src/chainparams.cpp#L94) |
| WIF (SECRET_KEY) | 0x85 | 133 (0x85) | [2.1.0 L138](https://github.com/nochowderforyou/clams/blob/d9ba48af9612a7c4af802613797ce928fd6993f8/src/chainparams.cpp#L138), [master L96](https://github.com/nochowderforyou/clams/blob/ac5c8cc04661eb181cda8651e931fcda3ad11a00/src/chainparams.cpp#L96) |
| BIP32 xpub | 0x0488B21E | 04 88 B2 1E | [2.1.0 L143](https://github.com/nochowderforyou/clams/blob/d9ba48af9612a7c4af802613797ce928fd6993f8/src/chainparams.cpp#L143) |
| BIP32 xprv | 0x0488ADE4 | 04 88 AD E4 | [2.1.0 L144](https://github.com/nochowderforyou/clams/blob/d9ba48af9612a7c4af802613797ce928fd6993f8/src/chainparams.cpp#L144) |
| Network magic | 03 22 35 15 | 0x03 0x22 0x35 0x15 | [2.1.0 L118-121](https://github.com/nochowderforyou/clams/blob/d9ba48af9612a7c4af802613797ce928fd6993f8/src/chainparams.cpp#L118-L121) |
| Default P2P port | 31174 | 31174 | [2.1.0 L122](https://github.com/nochowderforyou/clams/blob/d9ba48af9612a7c4af802613797ce928fd6993f8/src/chainparams.cpp#L122) |
| Script types | P2PKH, P2SH | base58 only; no bech32 HRP defined | [2.1.0 chainparams.cpp](https://github.com/nochowderforyou/clams/blob/d9ba48af9612a7c4af802613797ce928fd6993f8/src/chainparams.cpp) |
| SLIP-44 coin type | 23 | 23 = CLAM | [slip-0044.md @ 570ed55](https://github.com/satoshilabs/slips/blob/570ed55b7fde158f1116be34fc2faa35dada5912/slip-0044.md) (pending SLIP-0044 verification by a second reviewer) |

The values are identical at tag v2.1.0rc1 (3685d7b). The client also accepts
imported BTC/LTC/DOGE WIF keys (128/176/158); those are import aliases, not
CLAM's own WIF.

**Correction.** An earlier draft of this record carried WIF 0x99 and SLIP-44 217.
Both were wrong: 217 is Megacoin. The source values above replace them.

DOGE values mirror pycoin's `pycoin/symbols/doge.py` (WIF 0x9e, P2PKH 0x1e,
P2SH 0x16, BIP32 02fac398/02facafd). Solana uses SLIP-44 501 with SLIP-0010
ed25519 hardened derivation.

## How to verify

1. **Record against source.** Open each link in the table and compare the
   line to the value in `registry_record.py`. Then:

   ```
   python3 -c "import registry_record as r; c=r.CLAM; print(hex(c.address_version), hex(c.script_version), hex(c.wif_version), hex(c.bip32_pub_version), hex(c.bip32_priv_version), c.magic.hex(), c.port, c.slip44)"
   ```

   Expected output: `0x89 0xd 0x85 0x488b21e 0x488ade4 03223515 31174 23`

2. **Test vectors.** Reproduce `test_vectors.json` with any independent
   BIP-39 / SLIP-0010 implementation:
   - BIP-39: PBKDF2-HMAC-SHA512(mnemonic, "mnemonic"+passphrase, 2048) gives `seed_hex`.
   - SLIP-0010: HMAC-SHA512 with key "Bitcoin seed" or "ed25519 seed" over the seed gives the master key; then run hardened/normal CKD.

   The values come from the published BIP-39 (TREZOR vector 1) and
   SLIP-0010 (test vector 1) documents.
3. **A wrong value is a bug.** Open an issue with a link to the source line.

## License

Public domain facts about public chains. The code is released under the MIT
license by SMARTZ (Smartz Francis).
