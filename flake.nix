{
  description = "NLP Project";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/d189bf92f9be23f9b0f6c444f6ae29351bb7125c";
    utils = { url = "github:numtide/flake-utils"; };
    devshell-flake = { url = "github:numtide/devshell"; };
    gitignore = {
      url = "github:hercules-ci/gitignore.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, utils, devshell-flake, gitignore }:
    utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [
            devshell-flake.overlay
          ];
        };

        python = pkgs.python39;
        projectDir = gitignore.lib.gitignoreSource ./.;
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
              editablePackageSources = {
                experio = ./.;
              };
            })
            pkgs.poetry
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

          env = [
            {
              name = "JULIA_PROJECT";
              value = ".";
            }
          ];
        };
      });
}
