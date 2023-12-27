## Nix

`nix-build -E 'with import <nixpkgs> {}; callPackage ./env.nix {}'`