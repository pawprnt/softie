{ lib
, buildPythonPackage
, fetchFromGitHub
, setuptools
, pyside6
}:

buildPythonPackage {
  pname = "softie";
  version = "0.1.0";
  pyproject = true;

  src = fetchFromGitHub {
    owner = "pawprnt";
    repo = "softie";
    rev = "v0.1.0";
    hash = "sha256-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=";
  };

  build-system = [ setuptools ];

  propagatedBuildInputs = [
    pyside6
  ];

  pythonImportsCheck = [ "softie" ];

  meta = with lib; {
    description = "A kawaii self-care desktop companion";
    homepage = "https://github.com/pawprnt/softie";
    license = licenses.mit;
    mainProgram = "softie";
  };
}
