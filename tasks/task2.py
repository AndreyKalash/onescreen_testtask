from sqlalchemy import (
    Engine,
    MetaData,
    Table,
    create_engine,
    delete,
    func,
    literal_column,
    select,
)


def remove_duplicate_rows(engine: Engine, table: Table) -> None:
    """
    Удаление дубликатов строк в таблице, оставляя первую строку.

    :param engine: Объект SQLAlchemy Engine для соединения с базой данных
    :param table: Объект SQLAlchemy Table, из которого будут удаляться дубликаты
    """
    # создание cte подзапроса
    cte = select(
        table.c.id_o,
        table.c.sale,
        literal_column("ctid").label("ctid"),
        func.row_number()
        .over(
            partition_by=[table.c.id_o, table.c.sale], order_by=literal_column("ctid")
        )
        .label("rn"),
    ).cte(name="cte")
    # удаление дубликатов оставляя первую строку
    delete_stmt = delete(table).where(
        literal_column("ctid").in_(select(cte.c.ctid).where(cte.c.rn > 1))
    )
    with engine.connect() as session:
        session.execute(delete_stmt)
        session.commit()


def main() -> None:
    URL = "postgresql://postgres:1@localhost:5432/postgres"
    engine = create_engine(URL)

    metadata = MetaData()
    table = Table("accrual_report", metadata, autoload_with=engine)
    remove_duplicate_rows(engine, table)


if __name__ == "__main__":
    main()
