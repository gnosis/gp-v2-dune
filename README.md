# GPv2 Dune tools

A repository collecting the tools we used to build the [Dune dashboards for GPv2](https://duneanalytics.com/gnosis.protocol/Gnosis-Protocol-V2).

## Testing

There is a sample file `./test/regression.txt` which can be used to test the `formatQueryTokens` command as follows:

```sh
  export INFURA_KEY=<YOUR_INFURA_KEY>
npx hardhat formatQueryTokens --network mainnet --input-file ./test/regression.txt
```
