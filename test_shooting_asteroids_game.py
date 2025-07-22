import unittest
import math
from shooting_asteroids_game import check_ship_asteroid_collisions, check_bullet_asteroid_collision

class TestShootingAsteroidsGame(unittest.TestCase):

    def setUp(self):
        self.ship_x = 100
        self.ship_y = 100
        self.asteroid_close = [(105, 105, 0)]
        self.asteroid_far = [(300, 300, 0)]

        self.bullets = [(100, 100, 0)]
        self.asteroids = [(100, 100, 0)]

    def test_ship_collision_detected(self):
        result = check_ship_asteroid_collisions(self.ship_x, self.ship_y, self.asteroid_close.copy())
        self.assertTrue(result)

    def test_ship_collision_not_detected(self):
        result = check_ship_asteroid_collisions(self.ship_x, self.ship_y, self.asteroid_far.copy())
        self.assertFalse(result)

    def test_bullet_asteroid_collision(self):
        test_bullets = self.bullets.copy()
        test_asteroids = self.asteroids.copy()
        check_bullet_asteroid_collision(test_bullets, test_asteroids)
        self.assertEqual(len(test_bullets), 0)
        self.assertEqual(len(test_asteroids), 0)

    def test_bullet_no_collision(self):
        test_bullets = [(0, 0, 0)]
        test_asteroids = [(300, 300, 0)]
        check_bullet_asteroid_collision(test_bullets, test_asteroids)
        self.assertEqual(len(test_bullets), 1)
        self.assertEqual(len(test_asteroids), 1)

if __name__ == "__main__":
    unittest.main()
