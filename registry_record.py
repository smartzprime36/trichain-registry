"""TriChain Wallet — THE REGISTRY.

Written Oct 18, 2026 (CLAM values source-verified Oct 22), from the archaeology finding: CLAM has no tooling
in 2026 because it was never given a registry record in 2014. pycoin,
coininfo and python-bitcoinlib each generated whole tool families from
one declarative record per chain; DOGE has one in pycoin, CLAM has one
nowhere. This file is that missing record — for all three bench chains —
in one place, in the open, in a form other tools can lift.

UTXO records follow pycoin's shape (symbol, wif, address, script, BIP32
versions) extended with what pycoin never needed: serialization quirks,
network magic/port, SLIP-44 coin type, and read/broadcast adapters.
Solana's record is account-model (ed25519), kept in the same table so
the bench's state layer treats all three chains as rows, not worlds.
"""
from dataclasses import dataclass, field

@dataclass(frozen=True)
class UtxoChainRecord:
    symbol: str
    wif_version: int            # pycoin: wif prefix byte
    address_version: int        # pycoin: p2pkh prefix byte
    script_version: int         # pycoin: p2sh prefix byte
    bip32_priv_version: int     # pycoin: xprv version bytes (int form)
    bip32_pub_version: int      # pycoin: xpub version bytes (int form)
    magic: bytes                # P2P message start
    port: int                   # default P2P port
    slip44: int                 # SLIP-0044 coin type (None = unverified)
    tx_has_ntime: bool          # CLAM serializes nTime after nVersion
    tx_has_speech: bool         # CLAM version>1 appends strClamSpeech
    tx_version: int
    read_adapters: tuple = ()
    broadcast_adapters: tuple = ()

# DOGE — mirrors pycoin/symbols/doge.py exactly (wif 9e, addr 1e, script 16,
# BIP32 02fac398 / 02facafd), extended with our network + adapter facts.
DOGE = UtxoChainRecord(
    symbol='DOGE',
    wif_version=0x9e, address_version=0x1e, script_version=0x16,
    bip32_priv_version=0x02fac398, bip32_pub_version=0x02facafd,
    magic=bytes([0xc0, 0xc0, 0xc0, 0xc0]), port=22556,
    slip44=3, tx_has_ntime=False, tx_has_speech=False, tx_version=1,
    read_adapters=('sochain-v3', 'chainz-cryptoid'),
    broadcast_adapters=('own-relay (planned)', 'blockchair-push (endpoint verified Oct 18: live, parses txs)', 'blockcypher-push (unproven)'),
)

# CLAM — the missing record.
# SOURCE-VERIFIED Oct 22, 2026 against nochowderforyou/clams src/chainparams.cpp
# (branch 2.1.0 @ d9ba48af, lines 116-144; same values at tag v2.1.0rc1 and master):
# magic 03223515, port 31174, P2PKH 137 (0x89), P2SH 13 (0x0d),
# WIF/SECRET_KEY 133 (0x85), BIP32 xpub 0488B21E / xprv 0488ADE4.
# Earlier draft values wif 0x99 and SLIP-44 217 were WRONG (217 is Megacoin).
# SLIP-44: 23 per satoshilabs/slips slip-0044.md @ 570ed55 (pending SLIP-0044
# verification by a second reviewer). Script types: base58 P2PKH and P2SH
# only; the client defines no bech32 HRP. Serialization: nTime + ClamSpeech.
CLAM = UtxoChainRecord(
    symbol='CLAM',
    wif_version=0x85, address_version=0x89, script_version=0x0d,
    bip32_priv_version=0x0488ade4, bip32_pub_version=0x0488b21e,
    magic=bytes([0x03, 0x22, 0x35, 0x15]), port=31174,
    slip44=23, tx_has_ntime=True, tx_has_speech=True, tx_version=2,
    read_adapters=('chainz-cryptoid',),
    broadcast_adapters=('own-relay (planned)',),
)

@dataclass(frozen=True)
class AccountChainRecord:
    symbol: str
    curve: str                  # ed25519
    slip44: int
    derivation: str             # SLIP-0010 hardened path template
    read_adapters: tuple = ()
    broadcast_adapters: tuple = ()

SOL = AccountChainRecord(
    symbol='SOL', curve='ed25519', slip44=501,
    derivation="m/44'/501'/{account}'/0'",
    read_adapters=('solana-jsonrpc',),
    broadcast_adapters=('solana-jsonrpc sendTransaction',),
)

REGISTRY = {r.symbol: r for r in (CLAM, DOGE, SOL)}
