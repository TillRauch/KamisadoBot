{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  home-manager = {
      url = "github:nix-community/home-manager";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, home-manager, flake-utils }: 
    flake-utils.lib.eachDefaultSystem (system:
      let pkgs = import nixpkgs { inherit system; };
      in {
        devShell  = pkgs.mkShell {
          packages = [ pkgs.python3
                       pkgs.python311Packages.numpy
                       pkgs.python311Packages.pillow
                       pkgs.python311Packages.pytest
                       pkgs.python311Packages.pygame
                     ];
        };
      });
}

