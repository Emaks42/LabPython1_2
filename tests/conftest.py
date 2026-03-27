import pytest
import os


@pytest.fixture
def files():
    filenames = {"common": "tests"+os.sep+"common_file",
                 "corr_1": "tests"+os.sep+"corrupted_file_1",
                 "corr_2": "tests"+os.sep+"corrupted_file_2"}
    file_1 = open(filenames["common"], "w")
    file_1.write("""Task {
    id: 140
    description: обработать заказ с идентификатором 402
    priority: 5
    status: CREATED
    }
    Task {
    id: 1001
    description: отправить уведомление пользователю EMAKS
    priority: 2
    status: DONE
    }
    Task {
    id: 319
    description: проверить состояние сервиса eeva.team recroll.en
    priority: 1
    status: DONE
    }
    """)
    file_1.close()
    file_2 = open(filenames["corr_1"], "w")
    file_2.write("10a - f")
    file_2.close()
    file_3 = open(filenames["corr_2"], "w")
    file_3.write("""Task {
    something
    }""")
    file_3.close()
    return filenames
