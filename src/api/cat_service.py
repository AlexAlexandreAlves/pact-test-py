from dataclasses import dataclass
from typing import Any, List, Dict
import requests

@dataclass()
class Cat:
    id: int
    name: str
    age: int

class CatService:
    """Simple HTTP client for interacting with a cat provider service."""

    def __init__(self, hostname: str) -> None:
        self._hostname = hostname

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Centralized HTTP request handler with error and timeout management."""
        url = f"{self._hostname}{endpoint}"
        try:
            response = requests.request(method, url, timeout=10, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            # You can log the error or handle it as needed
            raise RuntimeError(f"HTTP request failed: {e}") from e

    def get_cat(self, cat_id: int) -> Cat:
        """Get a cat by ID from the provider.

        Args:
            cat_id (int): The ID of the cat.

        Returns:
            Cat: The cat object.
        """
        data = self._request("GET", f"/cats/{cat_id}")
        try:
            return Cat(
                id=data["id"],
                name=data["name"],
                age=data["age"],
            )
        except KeyError as e:
            raise ValueError(f"Missing expected field in response: {e}")

    def get_cats(self) -> List[Cat]:
        """Get all cats from the provider.

        Returns:
            List[Cat]: List of cat objects.
        """
        data = self._request("GET", "/cats")
        if not isinstance(data, list):
            raise ValueError("Expected a list of cats in response")
        cats = []
        for cat in data:
            try:
                cats.append(Cat(**cat))
            except TypeError as e:
                # Handle missing or extra fields gracefully
                raise ValueError(f"Invalid cat data: {cat}") from e
        return cats

    def create_cat(self, cat: Cat) -> Cat:
        """Create a new cat.

        Args:
            cat (Cat): The cat object to create.

        Returns:
            Cat: The created cat object.
        """
        payload = {
            "id": cat.id,
            "name": cat.name,
            "age": cat.age,
        }
        data = self._request("POST", "/cats", json=payload)
        try:
            return Cat(
                id=data["id"],
                name=data["name"],
                age=data["age"],
            )
        except KeyError as e:
            raise ValueError(f"Missing expected field in response: {e}")

    def update_cat(self, cat_id: int, cat: Cat) -> Cat:
        """Update an existing cat.

        Args:
            cat_id (int): The ID of the cat to update.
            cat (Cat): The updated cat data.

        Returns:
            Cat: The updated cat object.
        """
        payload = {
            "name": cat.name,
            "age": cat.age,
        }
        data = self._request("PUT", f"/cats/{cat_id}", json=payload)
        try:
            return Cat(
                id=cat_id,
                name=data["name"],
                age=data["age"],
            )
        except KeyError as e:
            raise ValueError(f"Missing expected field in response: {e}")

    def delete_cat(self, cat_id: int) -> Dict[str, Any]:
        """Delete a cat by ID.

        Args:
            cat_id (int): The ID of the cat to delete.

        Returns:
            Dict[str, Any]: The response message.
        """
        return self._request("DELETE", f"/cats/{cat_id}")