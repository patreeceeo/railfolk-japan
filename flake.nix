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

          railfolkJapanInstallService = pkgs.writeShellApplication {
            name = "railfolk-japan-install-service";
            runtimeInputs = [
              pkgs.coreutils
              pkgs.glibc.bin
              python
              pkgs.shadow
              pkgs.systemd
            ];
            text = ''
              if [ "$(id -u)" -ne 0 ]; then
                echo "railfolk-japan-install-service must run as root" >&2
                exit 1
              fi

              if ! groupadd --system railfolk-japan 2>/dev/null; then
                if ! getent group railfolk-japan >/dev/null 2>&1; then
                  echo "Failed to create railfolk-japan group" >&2
                  exit 1
                fi
              fi

              if ! id -u railfolk-japan >/dev/null 2>&1; then
                useradd \
                  --system \
                  --gid railfolk-japan \
                  --home-dir /var/lib/railfolk-japan \
                  railfolk-japan
              fi

              install -d -m 0755 -o railfolk-japan -g railfolk-japan /var/lib/railfolk-japan
              install -d -m 0755 -o railfolk-japan -g railfolk-japan /var/lib/railfolk-japan/app
              install -d -m 0755 -o root -g root /etc/railfolk-japan

              if [ ! -f /etc/railfolk-japan/env ]; then
                umask 077
                secret_key="$(python -c 'import secrets; print(secrets.token_urlsafe(50))')"
                env_tmp="$(mktemp)"
                {
                  printf 'DJANGO_SECRET_KEY=%s\n' "$secret_key"
                  printf 'DJANGO_ALLOWED_HOSTS=railfolk.zzt64.com,localhost,127.0.0.1\n'
                  printf 'DJANGO_DATABASE_PATH=/var/lib/railfolk-japan/db.sqlite3\n'
                } > "$env_tmp"
                install -m 0640 -o root -g railfolk-japan "$env_tmp" /etc/railfolk-japan/env
                rm -f "$env_tmp"
              fi

              chown root:railfolk-japan /etc/railfolk-japan/env
              chmod 0640 /etc/railfolk-japan/env

              unit_name=railfolk-japan.service
              persistent_unit=/etc/systemd/system/$unit_name
              runtime_unit=/run/systemd/system/$unit_name

              if install -d -m 0755 -o root -g root /etc/systemd/system \
                && install -m 0644 ${railfolkJapanService} "$persistent_unit"; then
                installed_persistently=1
              else
                install -d -m 0755 -o root -g root /run/systemd/system
                install -m 0644 ${railfolkJapanService} "$runtime_unit"
                installed_persistently=0
              fi

              systemctl daemon-reload
              if [ "$installed_persistently" -eq 1 ]; then
                systemctl enable "$unit_name"
              else
                echo "Installed $unit_name as a runtime unit because /etc/systemd/system is not writable; add it to host configuration for boot persistence" >&2
              fi
              systemctl restart "$unit_name"
            '';
          };
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
