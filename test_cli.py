from click.testing import CliRunner
import application as app
from run import main
def test_invalid_file():
	runner = CliRunner()
	result = runner.invoke(main,['graph', 'fskdhfks'])
	assert "FileNotFoundError" in result.output
	assert result.exit_code == 1

def test_not_a_log_file():
	runner = CliRunner()
	result = runner.invoke(main,['graph', '/Users/jasmineparekh/Desktop/h2oPackage/README.md'])
	assert "Not a log file" in result.output
	assert result.exit_code == 1

def test_correct_log_file():
	runner = CliRunner()
	result = runner.invoke(main,['graph', '/Users/jasmineparekh/Desktop/h2oPackage/h2oai_server_anonymized.log'])
	assert "Graph Done" in result.output
	assert result.exit_code == 0