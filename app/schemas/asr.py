from typing import Dict, List

from pydantic import BaseModel, Field


class ASRRequest(BaseModel):
    """Schema for ASR request, containing the path to the audio file."""

    audio_path: str = Field(..., description="Absolute path to the audio file.")


class DialogEntry(BaseModel):
    """Schema for a single dialog entry in the ASR response."""

    source: str = Field(
        ..., description="Speaker source (e.g., 'receiver', 'transmitter')."
    )
    text: str = Field(..., description="Recognized text from the audio segment.")
    duration: float = Field(
        ..., ge=0, description="Duration of the audio segment in seconds."
    )
    raised_voice: bool = Field(
        ..., description="Indicates if the speaker raised their voice."
    )
    gender: str = Field(..., description="Speaker's gender (e.g., 'male', 'female').")


class ASRResponse(BaseModel):
    """Schema for ASR response, including dialog entries and total durations."""

    dialog: List[DialogEntry] = Field(
        ..., description="List of dialog entries from the audio."
    )
    result_duration: Dict[str, float] = Field(
        ...,
        description="Total duration for each speaker (e.g., receiver, transmitter).",
    )
