from src.schedule.stores import (
    DisciplineStore,
    DirectionStore,
    TeacherStore,
    FlowStore,
    GroupStore,
    TypeDirectionStore
)

from src.schedule.repositories import (
    DisciplineRepos,
    DirectionRepos,
    TeacherRepos,
    FlowRepos,
    GroupRepos,
    TypeDirectionRepos
)


class ScheduleService:
    discipline_store: DisciplineStore
    direction_store: DirectionStore
    teacher_store: TeacherStore
    flow_store: FlowStore
    group_store: GroupStore
    type_direction_store: TypeDirectionStore

    def __init__(
        self,
        discipline_repository: DisciplineStore,
        direction_repository: DirectionStore,
        teacher_repository: TeacherStore,
        flow_repository: FlowStore,
        group_repository: GroupStore,
        type_direction_store: TypeDirectionStore
    ) -> None:
        self.direction_store = direction_repository()
        self.discipline_store = discipline_repository()
        self.teacher_store = teacher_repository()
        self.flow_store = flow_repository()
        self.group_store = group_repository()
        self.type_direction_store = type_direction_store()


schedule_service = ScheduleService(
    discipline_repository=DisciplineRepos,
    direction_repository=DirectionRepos,
    teacher_repository=TeacherRepos,
    flow_repository=FlowRepos,
    group_repository=GroupRepos,
    type_direction_store=TypeDirectionRepos
)
