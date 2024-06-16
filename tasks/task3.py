import pandas as pd
from sqlalchemy import Engine, MetaData, Table, create_engine, update


def update_data(engine: Engine, table: Table, data: pd.DataFrame) -> None:
    """
    Обновление данных в таблице на основе DataFrame.

    :param engine: Объект SQLAlchemy Engine для соединения с базой данных
    :param table: Объект SQLAlchemy Table, в котором будут обновлены данные
    :param data: DataFrame, содержащий данные для обновления
    """
    with engine.connect() as conn:
        for _, row in data.iterrows():
            stmt = (
                update(table)
                .where(table.c.sku == int(row["sku_old"]))
                .values(sku=int(row["sku_new"]))
            )
            conn.execute(stmt)
        conn.commit()


def main() -> None:
    data = pd.read_csv("data\\df.txt", sep=";")
    URLS = ["postgresql://postgres:1@localhost:5432/postgres"]
    for URL in URLS:
        engine = create_engine(URL)
        metadata = MetaData()
        table = Table("rating", metadata, autoload_with=engine)
        update_data(engine, table, data)


if __name__ == "__main__":
    main()
