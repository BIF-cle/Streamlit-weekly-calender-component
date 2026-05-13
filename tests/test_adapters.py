"""
Tests for data adapter system.

Tests:
- Identity adapter
- Flat events adapter
- Medical rehab adapter
- Project timeline adapter
- Custom adapter registration
"""

import pytest
from streamlit_activity_calendar import (
    identity_adapter,
    flat_events_adapter,
    medical_rehab_adapter,
    project_timeline_adapter,
    get_adapter,
    register_adapter,
    CalendarEvent,
    category_to_color,
)


class TestIdentityAdapter:
    """Tests for identity adapter."""
    
    def test_identity_adapter_with_dicts(self):
        """Test identity adapter with dictionary events."""
        data = [
            {
                "id": "1",
                "start": "2026-04-13",
                "title": "Meeting"
            }
        ]
        
        result = identity_adapter(data)
        
        assert len(result) == 1
        assert isinstance(result[0], CalendarEvent)
        assert result[0].id == "1"
        assert result[0].title == "Meeting"
    
    def test_identity_adapter_with_events(self):
        """Test identity adapter with CalendarEvent objects."""
        event = CalendarEvent(id="1", start="2026-04-13", title="Meeting")
        data = [event]
        
        result = identity_adapter(data)
        
        assert len(result) == 1
        assert result[0].id == "1"
    
    def test_identity_adapter_with_non_list(self):
        """Test identity adapter with non-list input."""
        result = identity_adapter("not a list")
        assert result == []
        
        result = identity_adapter(None)
        assert result == []


class TestFlatEventsAdapter:
    """Tests for flat events adapter."""
    
    def test_flat_events_adapter_basic(self):
        """Test flat events adapter with basic data."""
        data = [
            {
                "id": "1",
                "start": "2026-04-13",
                "title": "Meeting",
                "color": "#2196F3",
                "category": "work",
            },
            {
                "id": "2",
                "start": "2026-04-14",
                "title": "Task",
                "color": "#4CAF50",
                "category": "personal",
            }
        ]
        
        result = flat_events_adapter(data)
        
        assert len(result) == 2
        assert result[0].title == "Meeting"
        assert result[1].title == "Task"
        assert result[0].color == "#2196F3"
    
    def test_flat_events_adapter_with_metadata(self):
        """Test flat events adapter preserves metadata."""
        data = [
            {
                "id": "1",
                "start": "2026-04-13",
                "title": "Exercise",
                "metadata": {"sets": 3, "reps": 10},
                "raw": {"original": "data"}
            }
        ]
        
        result = flat_events_adapter(data)
        
        assert result[0].metadata["sets"] == 3
        assert result[0].raw["original"] == "data"
    
    def test_flat_events_adapter_with_missing_fields(self):
        """Test flat events adapter with missing fields."""
        data = [
            {
                "id": "1",
                "start": "2026-04-13",
                # missing title
            }
        ]
        
        result = flat_events_adapter(data)
        
        assert result[0].title == "Untitled"


class TestMedicalRehabAdapter:
    """Tests for medical rehab adapter."""
    
    def test_medical_rehab_adapter_basic(self):
        """Test medical rehab adapter with basic structure."""
        data = {
            "players": [
                {
                    "id": "p1",
                    "name": "John Doe",
                    "rehab_plans": [
                        {
                            "weeks": [
                                {
                                    "days": [
                                        {
                                            "date": "2026-04-13",
                                            "activities": [
                                                {
                                                    "id": "a1",
                                                    "title": "Quad Sets",
                                                    "category": "strengthening",
                                                    "sets": 3,
                                                    "reps": 10,
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        
        result = medical_rehab_adapter(data)
        
        assert len(result) == 1
        assert result[0].title == "Quad Sets"
        assert result[0].playerName == "John Doe"
        assert result[0].category == "strengthening"
    
    def test_medical_rehab_adapter_with_medical_events(self):
        """Test medical rehab adapter with medical events."""
        data = {
            "players": [
                {
                    "id": "p1",
                    "name": "Jane Doe",
                    "medical_events": [
                        {
                            "id": "med1",
                            "date": "2026-04-13",
                            "type": "appointment",
                            "title": "PT Session",
                            "notes": "Initial assessment"
                        }
                    ],
                    "rehab_plans": []
                }
            ]
        }
        
        result = medical_rehab_adapter(data)
        
        assert len(result) == 1
        assert result[0].title == "PT Session"
        assert result[0].category == "medical"
        assert result[0].color == "#FF5252"  # Medical color
    
    def test_medical_rehab_adapter_multiple_players(self):
        """Test medical rehab adapter with multiple players."""
        data = {
            "players": [
                {
                    "id": "p1",
                    "name": "Player 1",
                    "rehab_plans": [
                        {
                            "weeks": [
                                {
                                    "days": [
                                        {
                                            "date": "2026-04-13",
                                            "activities": [
                                                {
                                                    "id": "a1",
                                                    "title": "Exercise 1",
                                                    "category": "strengthening",
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": "p2",
                    "name": "Player 2",
                    "rehab_plans": [
                        {
                            "weeks": [
                                {
                                    "days": [
                                        {
                                            "date": "2026-04-14",
                                            "activities": [
                                                {
                                                    "id": "a2",
                                                    "title": "Exercise 2",
                                                    "category": "flexibility",
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        
        result = medical_rehab_adapter(data)
        
        assert len(result) == 2
        assert result[0].playerName == "Player 1"
        assert result[1].playerName == "Player 2"


class TestProjectTimelineAdapter:
    """Tests for project timeline adapter."""
    
    def test_project_timeline_adapter_basic(self):
        """Test project timeline adapter with basic data."""
        data = {
            "projects": [
                {
                    "id": "proj1",
                    "name": "Website Redesign",
                    "tasks": [
                        {
                            "id": "task1",
                            "title": "Design mockups",
                            "start_date": "2026-04-13",
                            "end_date": "2026-04-15",
                            "status": "in_progress",
                            "assignee": "Alice"
                        }
                    ]
                }
            ]
        }
        
        result = project_timeline_adapter(data)
        
        assert len(result) == 1
        assert result[0].title == "Design mockups"
        assert result[0].start == "2026-04-13"
        assert result[0].end == "2026-04-15"
        assert result[0].category == "in_progress"
    
    def test_project_timeline_adapter_status_colors(self):
        """Test project timeline adapter applies status colors."""
        data = {
            "projects": [
                {
                    "id": "proj1",
                    "name": "Project",
                    "tasks": [
                        {
                            "id": "t1",
                            "title": "Pending Task",
                            "start_date": "2026-04-13",
                            "status": "pending"
                        },
                        {
                            "id": "t2",
                            "title": "Completed Task",
                            "start_date": "2026-04-14",
                            "status": "completed"
                        }
                    ]
                }
            ]
        }
        
        result = project_timeline_adapter(data)
        
        assert result[0].category == "pending"
        assert result[0].color == "#FFC107"  # Pending color
        assert result[1].category == "completed"
        assert result[1].color == "#4CAF50"  # Completed color


class TestAdapterRegistry:
    """Tests for adapter registration system."""
    
    def test_get_adapter_by_name(self):
        """Test getting adapter by name."""
        adapter = get_adapter("identity")
        assert adapter is not None
        assert callable(adapter)
    
    def test_get_invalid_adapter(self):
        """Test getting invalid adapter raises error."""
        with pytest.raises(ValueError):
            get_adapter("nonexistent")
    
    def test_register_custom_adapter(self):
        """Test registering custom adapter."""
        def custom_adapter(data):
            return []
        
        register_adapter("custom", custom_adapter)
        
        adapter = get_adapter("custom")
        assert adapter is custom_adapter


class TestCategoryColors:
    """Tests for category to color mapping."""
    
    def test_category_to_color_known(self):
        """Test color mapping for known categories."""
        assert category_to_color("strengthening") == "#4CAF50"
        assert category_to_color("flexibility") == "#2196F3"
        assert category_to_color("cardio") == "#E91E63"
    
    def test_category_to_color_unknown(self):
        """Test color mapping for unknown category."""
        result = category_to_color("unknown_category")
        assert result == "#999999"  # Default gray
    
    def test_category_to_color_case_insensitive(self):
        """Test color mapping is case insensitive."""
        assert category_to_color("STRENGTHENING") == "#4CAF50"
        assert category_to_color("Flexibility") == "#2196F3"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
