import { createReadStream } from "fs";
import readline from "readline";

import { task } from "hardhat/config";

import { TokenDetails, tokenDetails } from "../ts/erc20";

async function inputFromFile(path: string): Promise<string[]> {
  const rl = readline.createInterface({
    input: createReadStream(path),
    output: process.stdout,
    terminal: false,
  });
  const addresses = [];
  for await (const line of rl) {
    // Unknown addresses use \x instead of 0x
    const matches = [...line.matchAll(/\\x[a-fA-F0-9]{40}/g)];
    addresses.push(...matches.map((match) => `0x${match[0].substring(2)}`));
  }
  return addresses;
}

function formatToken(token: TokenDetails, network: string): string | null {
  if (token.symbol === null) {
    console.warn(
      `Token without address or decimals at address ${
        token.address
      }, see block explorer at ${blockExplorerLink(token.address, network)}`,
    );
    return null;
  }
  if (!/^[ -!$&a-zA-Z0-9]*$/.exec(token.symbol)) {
    console.warn(
      `Token at address ${token.address} contains invalid characters in its symbol: ${token.symbol}`,
    );
    return null;
  }
  return `('${token.symbol}', ${token.decimals}, decode('${token.address
    .substring(2)
    .toLowerCase()}', 'hex')),`;
}

function blockExplorerLink(address: string, network: string) {
  switch (network) {
    case "mainnet":
      return `https://etherscan.io/token/${address}#readContract`;
    case "rinkeby":
      return `https://rinkeby.etherscan.io/token/${address}#readContract`;
    case "xdai":
      return `https://blockscout.com/xdai/mainnet/tokens/${address}/read-contract`;
    default:
      return ` == no block explorer available for network ${network} == `;
  }
}

const setupFormatQueryTokens: () => void = () => {
  task(
    "formatQueryTokens",
    "Format unknown token addresses to be used in the Dune query https://duneanalytics.com/queries/41469 .",
  )
    .addParam("inputFile", "The input file with the data to read.")
    .setAction(async ({ inputFile }, hre) => {
      const unknownAddresses = await inputFromFile(inputFile);
      let tokens = await Promise.all(
        unknownAddresses.map((address) => tokenDetails(address, hre)),
      );
      tokens = tokens
        .sort((lhs, rhs) =>
          lhs.address === rhs.address
            ? 0
            : lhs.address.toLowerCase() < rhs.address.toLowerCase()
            ? -1
            : 1,
        )
        .filter(
          (token, index) =>
            index === tokens.findIndex((t) => token.address === t.address),
        );
      const outputStrings = tokens
        .map((token) => formatToken(token, hre.network.name))
        .filter((output) => output !== null);
      for (const line of outputStrings) {
        console.log(line);
      }
    });
};

export { setupFormatQueryTokens };
