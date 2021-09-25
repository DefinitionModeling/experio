{ pkgs }:
pkgs.mkShell {
  packages = [
    # tex dev
    (pkgs.texlive.combine {
      inherit (pkgs.texlive)
        scheme-small
        ;
    })

    # nix dev
    pkgs.nixpkgs-fmt
  ];
}
