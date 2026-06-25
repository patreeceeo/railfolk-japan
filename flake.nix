{
  description = "Railfolk Japan Django application";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";
  };

  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-linux" ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
      pkgsFor = system: import nixpkgs { inherit system; };
    in
    {
      devShells = forAllSystems (system:
        let
          pkgs = pkgsFor system;
          python = pkgs.python313.withPackages (pythonPackages: [
            pythonPackages.django
            pythonPackages.gunicorn
          ]);
        in
        {
          default = pkgs.mkShell {
            packages = [
              python
            ];
          };
        });
    };
}
