class Transporter:
    def __init__(self, no, available_weight, empty_speed, work_speed):
        self.no = no
        self.available_weight = available_weight
        self.empty_speed = empty_speed
        self.work_speed = work_speed
        self.works = []

    def __str__(self, flag=True):
        ret = 'no: {}, available_weight: {}, empty_speed: {}, work_speed: {}, works: {}'.format(self.no,
                                                                                                self.available_weight,
                                                                                                self.empty_speed,
                                                                                                self.work_speed,
                                                                                                self.works)
        return ret


