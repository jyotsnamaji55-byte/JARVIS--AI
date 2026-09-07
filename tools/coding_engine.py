from tools.file_reader import read_file
from tools.file_writer import write_file
from tools.code_checker import check_python_code
from tools.code_generator import generate_python_code


def generate_and_validate(request):
    result = generate_python_code(request)

    if not result["success"]:
        return result

    check = check_python_code(result["code"])

    return {
        "success": check["valid"],
        "code": result["code"],
        "error": check["error"]
    }


def save_generated_code(filename, code, overwrite=False):
    check = check_python_code(code)

    if not check["valid"]:
        return {
            "success": False,
            "error": check["error"]
        }

    result = write_file(filename, code, overwrite)

    return {
        "success": result.startswith("File written successfully"),
        "message": result
    }


def read_code(filename):
    return read_file(filename)
