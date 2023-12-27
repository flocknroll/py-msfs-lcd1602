{ callPackage, python3Full, runCommand }:
let
    poetry2nix  = callPackage "${fetchTarball "https://github.com/nix-community/poetry2nix/archive/master.tar.gz"}" {};
in
poetry2nix.mkPoetryApplication {
    projectDir = ./.;
    python = python3Full;
}