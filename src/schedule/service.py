from src.schedule.stores import (
    DisciplineStore,
    DirectionStore,
    TeacherStore,
    FlowStore,
    GroupStore,
    TypeDirectionStore,
    TypeLessonStore,
    LoadListStore,
    TeacherLoadListStore,
    RoomStore,
    ScheduleListStore,
    ScheduleStore,
    ScheduleTeacherStore,
    ChangeStore
)

from src.schedule.repositories import (
    DisciplineRepos,
    DirectionRepos,
    TeacherRepos,
    FlowRepos,
    GroupRepos,
    TypeDirectionRepos,
    TypeLessonRepos,
    LoadListRepos,
    TeacherLoadListRepos,
    RoomRepos,
    ScheduleListRepos,
    ScheduleRepos,
    ScheduleTeacherRepos,
    ChangeRepos
)


class ScheduleService:
    discipline_store: DisciplineStore
    direction_store: DirectionStore
    teacher_store: TeacherStore
    flow_store: FlowStore
    group_store: GroupStore
    type_direction_store: TypeDirectionStore
    type_lesson_store: TypeLessonStore
    load_list_store: LoadListStore
    teacher_load_list_store: TeacherLoadListStore
    room_store: RoomStore
    schedule_list_store: ScheduleListStore
    schedule_store: ScheduleStore
    schedule_teacher_store: ScheduleTeacherStore
    change_store: ChangeStore

    def __init__(
        self,
        discipline_repository: DisciplineStore,
        direction_repository: DirectionStore,
        teacher_repository: TeacherStore,
        flow_repository: FlowStore,
        group_repository: GroupStore,
        type_direction_repository: TypeDirectionStore,
        type_lesson_repository: TypeLessonStore,
        load_list_repository: LoadListStore,
        teacher_load_list_repository: TeacherLoadListStore,
        room_repository: RoomStore,
        schedule_list_repository: ScheduleListStore,
        schedule_repository: ScheduleStore,
        schedule_teacher_repository: ScheduleTeacherStore,
        change_repository: ChangeStore

    ) -> None:
        self.direction_store = direction_repository()
        self.discipline_store = discipline_repository()
        self.teacher_store = teacher_repository()
        self.flow_store = flow_repository()
        self.group_store = group_repository()
        self.type_direction_store = type_direction_repository()
        self.type_lesson_store = type_lesson_repository()
        self.load_list_store = load_list_repository()
        self.teacher_load_list_store = teacher_load_list_repository()
        self.room_store = room_repository()
        self.schedule_list_store = schedule_list_repository()
        self.schedule_store = schedule_repository()
        self.schedule_teacher_store = schedule_teacher_repository()
        self.change_store = change_repository()


schedule_service = ScheduleService(
    discipline_repository=DisciplineRepos,
    direction_repository=DirectionRepos,
    teacher_repository=TeacherRepos,
    flow_repository=FlowRepos,
    group_repository=GroupRepos,
    type_direction_repository=TypeDirectionRepos,
    type_lesson_repository=TypeLessonRepos,
    load_list_repository=LoadListRepos,
    teacher_load_list_repository=TeacherLoadListRepos,
    room_repository=RoomRepos,
    schedule_list_repository=ScheduleListRepos,
    schedule_repository=ScheduleRepos,
    schedule_teacher_repository=ScheduleTeacherRepos,
    change_repository=ChangeRepos
)
