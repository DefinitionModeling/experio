{ pkgs ? import ./nix { } }:
pkgs.mkShell {
  packages = [
    # tex dev
    (pkgs.texlive.combine { inherit (pkgs.texlive) 
      scheme-full 
      # extra packages here
    ; })

    # nix dev
    pkgs.nixpkgs-fmt
  ];
}