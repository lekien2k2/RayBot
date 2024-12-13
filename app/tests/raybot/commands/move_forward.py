import unittest
from unittest.mock import MagicMock, patch

from app.services.commands.schemas import CommandStatusEnum
from app.services.raybot.schemas import CommandEnum
from app.services.raybot.service import raybot


class TestHandleMoveForward(unittest.TestCase):
    def setUp(self):
        # Khởi tạo đối tượng RaybotService
        self.raybot_service = raybot

        # Mock các thành phần phụ thuộc
        self.raybot_service.raybot_info = MagicMock()
        self.raybot_service.send_command = MagicMock(return_value=True)
        self.raybot_service.stop_event = MagicMock()
        self.raybot_service.stop_event.is_set = MagicMock(return_value=False)

        # Mock command_manager
        self.raybot_service.command_manager = MagicMock()

    @patch("time.sleep", return_value=None)
    def test_handle_move_forward_no_lift(self, _):
        self.raybot_service.raybot_info.lift_distance = 10
        self.raybot_service.raybot_info.min_distance_lift = 20

        self.raybot_service.handle_move_forward("test_id", {"location": "QR_1024"})

        self.raybot_service.send_command.assert_any_call(CommandEnum.forward)
        self.raybot_service.send_command.assert_not_called_with(CommandEnum.lift_box)

    @patch("time.sleep", return_value=None)
    def test_handle_move_forward_success(self, _):
        self.raybot_service.raybot_info.lift_distance = 10
        self.raybot_service.raybot_info.min_distance_lift = 50
        self.raybot_service.raybot_info.current_cmd = CommandEnum.lift_box
        self.raybot_service.raybot_info.qr_location = "QR_1024"

        self.raybot_service.stop_event.is_set = MagicMock(
            side_effect=[False, False, False, True]
        )

        self.raybot_service.handle_move_forward("test_id", {"location": "QR_1024"})

        self.raybot_service.send_command.assert_any_call(CommandEnum.lift_box)
        self.raybot_service.send_command.assert_any_call(CommandEnum.forward)
        self.raybot_service.send_command.assert_any_call(CommandEnum.stop)

    @patch("time.sleep", return_value=None)
    def test_handle_move_forward_lift_error(self, _):
        self.raybot_service.raybot_info.lift_distance = 10
        self.raybot_service.raybot_info.min_distance_lift = 50
        self.raybot_service.raybot_info.current_cmd = ""

        self.raybot_service.send_command = MagicMock(return_value=False)
        self.raybot_service.stop_event.is_set = MagicMock(return_value=False)

        self.raybot_service.handle_move_forward("test_id", {"location": "QR_1024"})

        self.raybot_service.send_command.assert_any_call(CommandEnum.lift_box)
        self.raybot_service.send_command.assert_any_call(CommandEnum.stop)

    @patch("time.sleep", return_value=None)
    def test_handle_move_forward_stop_event_during_lift(self, _):
        self.raybot_service.raybot_info.lift_distance = 10
        self.raybot_service.raybot_info.min_distance_lift = 50
        self.raybot_service.stop_event.is_set = MagicMock(side_effect=[False, True])

        self.raybot_service.handle_move_forward("test_id", {"location": "QR_1024"})

        self.raybot_service.send_command.assert_any_call(CommandEnum.stop)

    @patch("time.sleep", return_value=None)
    def test_handle_move_forward_no_qr_code(self, _):
        self.raybot_service.raybot_info.qr_location = "QR_UNKNOWN"
        self.raybot_service.stop_event.is_set = MagicMock(
            side_effect=[False, False, True]
        )

        self.raybot_service.handle_move_forward("test_id", {"location": "QR_1024"})

        self.raybot_service.send_command.assert_any_call(CommandEnum.forward)


if __name__ == "__main__":
    unittest.main()
