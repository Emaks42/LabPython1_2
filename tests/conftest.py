import pytest
import os


@pytest.fixture
def files():
    filenames = {"common": "tests"+os.sep+"common_file",
                 "corr_1": "tests"+os.sep+"corrupted_file_1",
                 "corr_2": "tests"+os.sep+"corrupted_file_2"}
    file_1 = open(filenames["common"], "w")
    file_1.write("""103 - проверить состояние ресурса MAII
3457 - проверить состояние сервиса mai.ru NIICHAVO.su
104 - обработать заказ с идентификатором 403""")
    file_1.close()
    file_2 = open(filenames["corr_1"], "w")
    file_2.write("10a - f")
    file_2.close()
    file_3 = open(filenames["corr_2"], "w")
    file_3.write("10af")
    file_3.close()
    return filenames
