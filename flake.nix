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
      packages = forAllSystems (system:
        let
          pkgs = pkgsFor system;
          python = pkgs.python313.withPackages (pythonPackages: [
            pythonPackages.django
            pythonPackages.gunicorn
          ]);
        in
        rec {
          railfolkJapanServer = pkgs.writeShellApplication {
            name = "railfolk-japan-server";
            runtimeInputs = [
              python
            ];
            text = ''
              exec gunicorn railfolk_japan.wsgi:application --bind 127.0.0.1:8000
            '';
          };

          railfolkJapanService = pkgs.writeText "railfolk-japan.service" ''
            [Unit]
            Description=Railfolk Japan
            After=network-online.target
            Wants=network-online.target

            [Service]
            User=railfolk-japan
            Group=railfolk-japan
            WorkingDirectory=/var/lib/railfolk-japan/app
            EnvironmentFile=/etc/railfolk-japan/env
            ExecStart=${railfolkJapanServer}/bin/railfolk-japan-server
            KillSignal=SIGQUIT
            TimeoutStopSec=30
            Restart=always
            RestartSec=5

            [Install]
            WantedBy=multi-user.target
          '';
        });

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
