from config import config
from src.db_manager import DBManager
from src.utils import get_hh_json, create_db, save_data_to_db


def main():
    params = config()
    # ID компаний работодателей: "Яндекс", "VK", "OZON", "2GIS", "Контур",
    # "Kaspersky", "ЦИАН", "Битрикс24", "NAUMEN", "Skyeng"
    employers = ['1740', '15478', '2180', '64174', '41862',
                 '1057', '1429999', '129044', '42600', '1122462']
    data = get_hh_json(employers)
    create_db('hh_vacancies', params)
    save_data_to_db(data, 'hh_vacancies', params)
    db_manager = DBManager('hh_vacancies', params)
    pass
