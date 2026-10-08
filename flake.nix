{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = { self, nixpkgs }:
  let
    system = "x86_64-linux";
    pkgs = import nixpkgs { inherit system; config.allowUnfree = true; };

    libs = with pkgs; [
      zlib
      libxext
    ];
  in
  {
    devShells.${system}.default = pkgs.mkShell {
      packages = with pkgs; [
        python313
      ];

      shellHook = ''
        export LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath libs}:$LD_LIBRARY_PATH"
        source .venv/bin/activate
      '';
    };
  };
}