import streamlit as st
import requests
import datetime


API_URL = "http://localhost:8000/api/v1"

def get_ensembles():
    try:
        response = requests.get(f"{API_URL}/ensembles/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching ensembles: {e}")
        return []

def add_ensemble(name, leader):
    data = {"name": name, "leader": leader}
    try:
        response = requests.post(f"{API_URL}/ensembles/", json=data)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Error adding ensemble: {e}")
        return False

def get_music_count(ensemble_id):
    try:
        response = requests.get(f"{API_URL}/ensembles/{ensemble_id}/music_count")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching music count: {e}")
        return 0

def get_cds_by_ensemble(ensemble_id):
    try:
        response = requests.get(f"{API_URL}/ensembles/{ensemble_id}/cds/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching CDs: {e}")
        return []

def add_musician(name, instrument, ensemble_id):
    data = {"name": name, "instrument": instrument, "ensemble_id": ensemble_id}
    try:
        response = requests.post(f"{API_URL}/musicians/", json=data)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Error adding musician: {e}")
        st.error(e.response.text)
        return False

def add_cd(title, release_date, wholesale_price, retail_price, sold_last_year, sold_this_year, stock, ensemble_id, company, company_address):
    cds = get_cds_by_ensemble(ensemble_id)
    for cd in cds:
        if cd['title'].lower() == title.lower():
            st.error(f"CD with title '{title}' already exists for this ensemble.")
            return False

    data = {
        "title": title,
        "release_date": release_date.isoformat(),
        "wholesale_price": wholesale_price,
        "retail_price": retail_price,
        "sold_last_year": sold_last_year,
        "sold_this_year": sold_this_year,
        "stock": stock,
        "ensemble_id": ensemble_id,
        "company": company,
        "company_address": company_address
    }
    try:
        response = requests.post(f"{API_URL}/cds/", json=data)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Error adding CD: {e}")
        st.error(e.response.text)
        return False

def update_cd(cd_id, title, release_date, wholesale_price, retail_price, sold_last_year, sold_this_year, stock, ensemble_id, company, company_address):
    data = {
        "title": title,
        "release_date": release_date.isoformat(),
        "wholesale_price": wholesale_price,
        "retail_price": retail_price,
        "sold_last_year": sold_last_year,
        "sold_this_year": sold_this_year,
        "stock": stock,
        "ensemble_id": ensemble_id,
        "company": company,
        "company_address": company_address
    }
    try:
        response = requests.put(f"{API_URL}/cds/{cd_id}", json=data)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Error updating CD: {e}")
        st.error(e.response.text)
        return False

def delete_cd(cd_id):
    if cd_id is None:
        st.error("Ошибка: Компакт-диск не выбран.")
        return False
    try:
        response = requests.delete(f"{API_URL}/cds/{cd_id}")
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Error deleting CD: {e}")
        return False

def add_performance(cd_id, music_id, performer):
    data = {
        "cd_id": cd_id,
        "music_id": music_id,
        "performer": performer
    }
    try:
        response = requests.post(f"{API_URL}/performances/", json=data)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Error adding performance: {e}")
        st.error(e.response.text)
        return False

def get_performances_by_cd(cd_id):
    try:
        response = requests.get(f"{API_URL}/cd/{cd_id}/performances")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching performances: {e}")
        return []

def add_music(title, composer, ensemble_id):
    data = {"title": title, "composer": composer, "ensemble_id": ensemble_id}
    try:
        response = requests.post(f"{API_URL}/music/", json=data)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Error adding music: {e}")
        st.error(e.response.text)
        return False

def main():
    st.sidebar.title("Навигация")
    page = st.sidebar.radio("Перейти к", ["Главная", "Ансамбли", "Музыканты", "Компакт-диски", "Музыкальные произведения"])

    if page == "Главная":
        st.title("Музыкальный Магазин")
        st.write("Добро пожаловать в музыкальный магазин. Выберите страницу в навигационной панели слева.")

    elif page == "Ансамбли":
        st.header("Ансамбли")
        ensembles = get_ensembles()

        for ensemble in ensembles:
            st.subheader(f"{ensemble['name']} (Лидер: {ensemble['leader']})")

            with st.expander("Музыканты"):
                for musician in ensemble['musicians']:
                    st.write(f"- {musician['name']} ({musician['instrument']})")

            music_count = get_music_count(ensemble['id'])
            st.write(f"Количество музыкальных произведений: {music_count}")

            cds = get_cds_by_ensemble(ensemble['id'])
            with st.expander("Компакт-диски"):
                for cd in cds:
                    st.write(f"- {cd['title']} (Продано в этом году: {cd['sold_this_year']})")
                    performances = get_performances_by_cd(cd['id'])
                    st.write(f"Исполнения для {cd['title']}:")
                    for performance in performances:
                        st.write(f"  - Музыкальное произведение ID: {performance['music_id']}, Исполнитель: {performance['performer']}")

        st.subheader("Добавить новый ансамбль")
        name = st.text_input("Название ансамбля")
        leader = st.text_input("Лидер ансамбля")
        if st.button("Добавить ансамбль"):
            if add_ensemble(name, leader):
                st.success("Ансамбль успешно добавлен!")
            else:
                st.error("Ошибка при добавлении ансамбля.")

    elif page == "Музыканты":
        st.header("Добавить Музыканта")
        ensembles = get_ensembles()
        musician_name = st.text_input("Имя музыканта")
        instrument = st.text_input("Инструмент")
        ensemble_id = st.selectbox("Ансамбль (Музыкант)", [ensemble['id'] for ensemble in ensembles], key="musician_ensemble")
        if st.button("Добавить музыканта"):
            if add_musician(musician_name, instrument, ensemble_id):
                st.success("Музыкант успешно добавлен!")
            else:
                st.error("Ошибка при добавлении музыканта.")

    elif page == "Компакт-диски":
        st.header("Добавить Компакт-диск")
        ensembles = get_ensembles()
        cds = []
        cd_title = st.text_input("Название компакт-диска")
        cd_release_date = st.date_input("Дата выпуска", value=datetime.date.today())
        cd_wholesale_price = st.number_input("Оптовая цена")
        cd_retail_price = st.number_input("Розничная цена")
        cd_sold_last_year = st.number_input("Продано в прошлом году", min_value=0)
        cd_sold_this_year = st.number_input("Продано в этом году", min_value=0)
        cd_stock = st.number_input("Остаток на складе", min_value=0)
        cd_ensemble_id = st.selectbox("Ансамбль (Компакт-диск)", [ensemble['id'] for ensemble in ensembles], key="cd_ensemble")
        cd_company = st.text_input("Компания")
        cd_company_address = st.text_input("Адрес компании")
        if st.button("Добавить компакт-диск"):
            if add_cd(cd_title, cd_release_date, cd_wholesale_price, cd_retail_price, cd_sold_last_year, cd_sold_this_year, cd_stock, cd_ensemble_id, cd_company, cd_company_address):
                st.success("Компакт-диск успешно добавлен!")
                cds = get_cds_by_ensemble(cd_ensemble_id)  # Обновляем список CD после добавления
            else:
                st.error("Ошибка при добавлении компакт-диска.")

        st.header("Добавить Исполнение на Компакт-диск")
        cds = get_cds_by_ensemble(cd_ensemble_id) if not cds else cds  # Инициализируем cds, если не инициализирован
        if cds:
            cd_id = st.selectbox("Выберите компакт-диск", [cd['id'] for cd in cds])
            music_id = st.number_input("ID музыкального произведения", min_value=0)
            performer = st.text_input("Исполнитель")
            if st.button("Добавить исполнение"):
                if add_performance(cd_id, music_id, performer):
                    st.success("Исполнение успешно добавлено!")
                else:
                    st.error("Ошибка при добавлении исполнения.")

        st.header("Удалить Компакт-диск")
        ensemble_id_for_delete = st.selectbox("Ансамбль для удаления CD", [ensemble['id'] for ensemble in ensembles], key="cd_ensemble_delete")
        cds_for_delete = get_cds_by_ensemble(ensemble_id_for_delete)
        cd_to_delete = st.selectbox("Выберите компакт-диск для удаления", [cd['title'] for cd in cds_for_delete])
        cd_id_to_delete = next((cd['id'] for cd in cds_for_delete if cd['title'] == cd_to_delete), None)
        if st.button("Удалить компакт-диск"):
            if delete_cd(cd_id_to_delete):
                st.success("Компакт-диск успешно удален!")
            else:
                st.error("Ошибка при удалении компакт-диска.")

    elif page == "Музыкальные произведения":
        st.header("Добавить Музыкальное Произведение")
        ensembles = get_ensembles()
        music_title = st.text_input("Название музыкального произведения")
        composer = st.text_input("Композитор")
        ensemble_id = st.selectbox("Ансамбль (Музыкальное произведение)", [ensemble['id'] for ensemble in ensembles], key="music_ensemble")
        if st.button("Добавить музыкальное произведение"):
            if add_music(music_title, composer, ensemble_id):
                st.success("Музыкальное произведение успешно добавлено!")
            else:
                st.error("Ошибка при добавлении музыкального произведения.")

if __name__ == "__main__":
    main()
