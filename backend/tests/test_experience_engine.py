import unittest
from unittest.mock import MagicMock, patch
from app.domain.experience_engine import ExperienceEngine

class TestExperienceEngine(unittest.TestCase):

    def setUp(self):
        self.user_id = 1
        self.module_slug = "tictactoe"
        self.result = {
            "completed": True,
            "score": 150,
            "win": True
        }

    @patch('app.domain.experience_engine.socketio.emit')
    @patch('app.domain.roast_service.RoastService.get_roast')
    @patch('app.domain.mentor_service.MentorService.get_advice')
    @patch('app.models.user.User.query')
    def test_process_module_result_emits_socket(self, mock_user_query, mock_advice, mock_roast, mock_emit):
        # Setup mocks
        mock_user = MagicMock()
        mock_user.username = "testuser"
        mock_user_query.get.return_value = mock_user
        mock_roast.return_value = "Test Roast"
        mock_advice.return_value = "Test Advice"

        # Execute
        ExperienceEngine.process_module_result(self.user_id, self.module_slug, self.result)

        # Verify socket emits
        # We expect at least one ux_event for roast and one for advice
        self.assertTrue(mock_emit.called)
        
        # Check if first call was for roast or mentor
        args, kwargs = mock_emit.call_args_list[0]
        self.assertEqual(args[0], "ux_event")
        self.assertEqual(kwargs["room"], f"user_{self.user_id}")

    def test_normalize_result(self):
        raw_result = {"score": 100}
        normalized = ExperienceEngine.normalize_result(raw_result)
        
        self.assertEqual(normalized["score"], 100)
        self.assertTrue(normalized["completed"])
        self.assertFalse(normalized["win"])

if __name__ == '__main__':
    unittest.main()
