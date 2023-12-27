{ callPackage, python3, runCommand }:
let
    poetry2nix  = callPackage "${fetchTarball "https://github.com/nix-community/poetry2nix/archive/refs/tags/2023.12.2614813.tar.gz"}" {};
in
poetry2nix.mkPoetryEnv {
    projectDir = ./.;
    python = python3;
    editablePackageSources = {
        py_msfs_lcd1602 = ./py_msfs_lcd1602;
    };
    # See https://github.com/nix-community/poetry2nix/blob/master/docs/edgecases.md
    overrides = poetry2nix.defaultPoetryOverrides.extend(self: super: {
        lunr = super.lunr.overridePythonAttrs(old: { buildInputs = (old.buildInputs or [ ]) ++ [ super.hatchling super.hatch-fancy-pypi-readme ]; });
        pysimconnect = super.pysimconnect.overridePythonAttrs(old: { buildInputs = (old.buildInputs or [ ]) ++ [ super.setuptools ]; });
    });
}