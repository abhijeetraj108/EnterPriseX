from uuid import uuid4

from enterprise_x.contracts.common import MessageRole
from enterprise_x.contracts.conversation import (
    Conversation,
    ConversationMessage,
    ConversationContext,
)


def test_conversation_creation():
    conversation = Conversation(
        user_id=uuid4(),
        tenant_id=uuid4(),
    )

    assert conversation.conversation_id is not None


def test_message_creation():
    message = ConversationMessage(
        conversation_id=uuid4(),
        role=MessageRole.USER,
        content="Show invoice INV-801",
    )

    assert message.role == MessageRole.USER


def test_conversation_context():
    context = ConversationContext(
        conversation_id=uuid4(),
        context_summary="User is investigating invoice INV-801",
    )

    assert context.active_investigation_id is None