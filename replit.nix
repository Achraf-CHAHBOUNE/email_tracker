{ pkgs }: {
  deps = [
    pkgs.python310
    pkgs.sqlite
  ];

  env = {
    FLASK_RUN_PORT = "8080";
  };

  packages = [
    pkgs.python310Packages.pip
  ];
}
