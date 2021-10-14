{
  description = "NLP Project";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/d189bf92f9be23f9b0f6c444f6ae29351bb7125c";
    utils = { url = "github:numtide/flake-utils"; };
    compat = { url = "github:edolstra/flake-compat"; flake = false; };
    devshell-flake = { url = "github:numtide/devshell"; };
  };

  outputs = { self, nixpkgs, utils, compat, devshell-flake }:
    utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [
            devshell-flake.overlay
          ];
        };

        python = pkgs.python39;
        projectDir = ./.;
        overrides = pkgs.poetry2nix.overrides.withDefaults (final: prev: {
          # Python dependency overrides go here
        });

        packageName = "experio";
      in
      {
        packages.${packageName} = pkgs.poetry2nix.mkPoetryApplication {
          inherit python projectDir overrides;
          propogatedBuildInputs = [
            # Non-Python runtime dependencies go here
          ];
        };

        defaultPackage = self.packages.${system}.${packageName};

        devShell = with pkgs; devshell.mkShell {
          packages = [
            # python
            (pkgs.poetry2nix.mkPoetryEnv {
              inherit python projectDir overrides;
            })
            pkgs.julia_16-bin

            # tex
            (pkgs.texlive.combine {
              inherit (pkgs.texlive)
                scheme-small
                latexmk
                latexindent

                preprint
                algorithmicx

                # fonts
                helvetic
                courier
                ;
            })
          ];

          commands = [{
            name = "pluto";
            category = "Julia";
            command = ''
              eval $(echo "julia -e 'import Pkg; Pkg.activate(\".\"); using Pluto; Pluto.run()'")
            '';
            help = "launch pluto server";
          }];

          env = [{
            name = "JULIA_PROJECT";
            value = ".";
          }];
        };
      });
}
