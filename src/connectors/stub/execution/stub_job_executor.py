from connectors.base.execution import ConnectorJobExecutor


class StubJobExecutor(ConnectorJobExecutor):
    def start(self) -> None:
        pass

    def process(self) -> None:
        pass

    def remove(self) -> None:
        pass
