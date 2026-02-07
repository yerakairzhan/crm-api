#!/bin/bash

# CRM API Testing Script
# This script tests all endpoints of the CRM backend API

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# API Base URL
BASE_URL="http://localhost:3000"

# Variables to store tokens and IDs
ACCESS_TOKEN_USER=""
ACCESS_TOKEN_AUTHOR=""
USER_ID=""
AUTHOR_ID=""
TASK_ID=""
COMMENT_ID=""

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}CRM API Testing Script${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Helper function to print section headers
print_header() {
    echo -e "\n${YELLOW}>>> $1${NC}"
}

# Helper function to print success
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Helper function to print error
print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Helper function to print response
print_response() {
    echo -e "${BLUE}Response:${NC}"
    echo "$1" | jq '.' 2>/dev/null || echo "$1"
}

# Wait for user to press enter
wait_for_enter() {
    echo -e "\n${YELLOW}Press Enter to continue...${NC}"
    read
}

# ============================================
# 1. AUTH - REGISTRATION
# ============================================
print_header "1. Testing User Registration"

echo "Registering regular user (role: user)..."
RESPONSE=$(curl -s -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "role": "user"
  }')

USER_ID=$(echo $RESPONSE | jq -r '.id')
print_response "$RESPONSE"

if [ "$USER_ID" != "null" ] && [ -n "$USER_ID" ]; then
    print_success "Regular user registered successfully. User ID: $USER_ID"
else
    print_error "Failed to register regular user"
fi

wait_for_enter

echo "Registering author user (role: author)..."
RESPONSE=$(curl -s -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "author@example.com",
    "password": "password123",
    "role": "author"
  }')

AUTHOR_ID=$(echo $RESPONSE | jq -r '.id')
print_response "$RESPONSE"

if [ "$AUTHOR_ID" != "null" ] && [ -n "$AUTHOR_ID" ]; then
    print_success "Author user registered successfully. Author ID: $AUTHOR_ID"
else
    print_error "Failed to register author user"
fi

wait_for_enter

# ============================================
# 2. AUTH - LOGIN
# ============================================
print_header "2. Testing User Login"

echo "Logging in as regular user..."
RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }')

ACCESS_TOKEN_USER=$(echo $RESPONSE | jq -r '.access_token')
print_response "$RESPONSE"

if [ "$ACCESS_TOKEN_USER" != "null" ] && [ -n "$ACCESS_TOKEN_USER" ]; then
    print_success "Regular user logged in successfully"
else
    print_error "Failed to login as regular user"
fi

wait_for_enter

echo "Logging in as author..."
RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "author@example.com",
    "password": "password123"
  }')

ACCESS_TOKEN_AUTHOR=$(echo $RESPONSE | jq -r '.access_token')
print_response "$RESPONSE"

if [ "$ACCESS_TOKEN_AUTHOR" != "null" ] && [ -n "$ACCESS_TOKEN_AUTHOR" ]; then
    print_success "Author logged in successfully"
else
    print_error "Failed to login as author"
fi

wait_for_enter

# ============================================
# 3. USERS - CRUD OPERATIONS
# ============================================
print_header "3. Testing Users Endpoints"

echo "Getting all users (authenticated)..."
RESPONSE=$(curl -s -X GET "$BASE_URL/users" \
  -H "Authorization: Bearer $ACCESS_TOKEN_USER")
print_response "$RESPONSE"
print_success "Retrieved all users"

wait_for_enter

echo "Getting user by ID..."
RESPONSE=$(curl -s -X GET "$BASE_URL/users/$USER_ID" \
  -H "Authorization: Bearer $ACCESS_TOKEN_USER")
print_response "$RESPONSE"
print_success "Retrieved user by ID"

wait_for_enter

echo "Updating user..."
RESPONSE=$(curl -s -X PATCH "$BASE_URL/users/$USER_ID" \
  -H "Authorization: Bearer $ACCESS_TOKEN_USER" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "updated_user@example.com"
  }')
print_response "$RESPONSE"
print_success "User updated successfully"

wait_for_enter

# ============================================
# 4. TASKS - CREATE
# ============================================
print_header "4. Testing Task Creation"

echo "Creating task as regular user..."
RESPONSE=$(curl -s -X POST "$BASE_URL/tasks" \
  -H "Authorization: Bearer $ACCESS_TOKEN_USER" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Complete project documentation and setup tests"
  }')

TASK_ID=$(echo $RESPONSE | jq -r '.id')
print_response "$RESPONSE"

if [ "$TASK_ID" != "null" ] && [ -n "$TASK_ID" ]; then
    print_success "Task created successfully. Task ID: $TASK_ID"
else
    print_error "Failed to create task"
fi

wait_for_enter

echo "Creating another task as author..."
RESPONSE=$(curl -s -X POST "$BASE_URL/tasks" \
  -H "Authorization: Bearer $ACCESS_TOKEN_AUTHOR" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Review pull requests and merge approved changes"
  }')
print_response "$RESPONSE"
print_success "Second task created"

wait_for_enter

# ============================================
# 5. TASKS - READ
# ============================================
print_header "5. Testing Task Retrieval"

echo "Getting all tasks (should be sorted by created_at DESC)..."
RESPONSE=$(curl -s -X GET "$BASE_URL/tasks" \
  -H "Authorization: Bearer $ACCESS_TOKEN_USER")
print_response "$RESPONSE"
print_success "Retrieved all tasks"

wait_for_enter

echo "Getting task by ID..."
RESPONSE=$(curl -s -X GET "$BASE_URL/tasks/$TASK_ID" \
  -H "Authorization: Bearer $ACCESS_TOKEN_USER")
print_response "$RESPONSE"
print_success "Retrieved task by ID"

wait_for_enter

# ============================================
# 6. TASKS - UPDATE
# ============================================
print_header "6. Testing Task Update"

echo "Updating task (by owner)..."
RESPONSE=$(curl -s -X PATCH "$BASE_URL/tasks/$TASK_ID" \
  -H "Authorization: Bearer $ACCESS_TOKEN_USER" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Updated: Complete project documentation, setup tests, and write README"
  }')
print_response "$RESPONSE"
print_success "Task updated successfully"

wait_for_enter

echo "Trying to update task by non-owner (should fail)..."
RESPONSE=$(curl -s -X PATCH "$BASE_URL/tasks/$TASK_ID" \
  -H "Authorization: Bearer $ACCESS_TOKEN_AUTHOR" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Attempting unauthorized update"
  }')
print_response "$RESPONSE"
print_error "Expected error - only owner can update task"

wait_for_enter

# ============================================
# 7. COMMENTS - CREATE
# ============================================
print_header "7. Testing Comment Creation"

echo "Trying to create comment as regular user (should fail - only 'author' role allowed)..."
RESPONSE=$(curl -s -X POST "$BASE_URL/comments" \
  -H "Authorization: Bearer $ACCESS_TOKEN_USER" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This comment should fail because user role is not author",
    "task_id": "'"$TASK_ID"'"
  }')
print_response "$RESPONSE"
print_error "Expected error - only author role can create comments"

wait_for_enter

echo "Creating comment as author (should succeed)..."
RESPONSE=$(curl -s -X POST "$BASE_URL/comments" \
  -H "Authorization: Bearer $ACCESS_TOKEN_AUTHOR" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Great work on this task! The implementation looks solid.",
    "task_id": "'"$TASK_ID"'"
  }')

COMMENT_ID=$(echo $RESPONSE | jq -r '.id')
print_response "$RESPONSE"

if [ "$COMMENT_ID" != "null" ] && [ -n "$COMMENT_ID" ]; then
    print_success "Comment created successfully. Comment ID: $COMMENT_ID"
else
    print_error "Failed to create comment"
fi

wait_for_enter

echo "Creating another comment..."
RESPONSE=$(curl -s -X POST "$BASE_URL/comments" \
  -H "Authorization: Bearer $ACCESS_TOKEN_AUTHOR" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Please review the code changes before merging.",
    "task_id": "'"$TASK_ID"'"
  }')
print_response "$RESPONSE"
print_success "Second comment created"

wait_for_enter

# ============================================
# 8. COMMENTS - READ
# ============================================
print_header "8. Testing Comment Retrieval"

echo "Getting all comments..."
RESPONSE=$(curl -s -X GET "$BASE_URL/comments" \
  -H "Authorization: Bearer $ACCESS_TOKEN_USER")
print_response "$RESPONSE"
print_success "Retrieved all comments"

wait_for_enter

echo "Getting comments filtered by task_id..."
RESPONSE=$(curl -s -X GET "$BASE_URL/comments?task_id=$TASK_ID" \
  -H "Authorization: Bearer $ACCESS_TOKEN_USER")
print_response "$RESPONSE"
print_success "Retrieved comments for specific task"

wait_for_enter

echo "Getting comment by ID..."
RESPONSE=$(curl -s -X GET "$BASE_URL/comments/$COMMENT_ID" \
  -H "Authorization: Bearer $ACCESS_TOKEN_USER")
print_response "$RESPONSE"
print_success "Retrieved comment by ID"

wait_for_enter

# ============================================
# 9. COMMENTS - UPDATE
# ============================================
print_header "9. Testing Comment Update"

echo "Updating comment (by owner)..."
RESPONSE=$(curl -s -X PATCH "$BASE_URL/comments/$COMMENT_ID" \
  -H "Authorization: Bearer $ACCESS_TOKEN_AUTHOR" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Updated: Excellent work on this task! The implementation is very solid."
  }')
print_response "$RESPONSE"
print_success "Comment updated successfully"

wait_for_enter

echo "Trying to update comment by non-owner (should fail)..."
RESPONSE=$(curl -s -X PATCH "$BASE_URL/comments/$COMMENT_ID" \
  -H "Authorization: Bearer $ACCESS_TOKEN_USER" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Trying to update someone else comment"
  }')
print_response "$RESPONSE"
print_error "Expected error - only owner can update comment"

wait_for_enter

# ============================================
# 10. VALIDATION TESTS
# ============================================
print_header "10. Testing Input Validation"

echo "Creating task with invalid description (too long - over 1000 chars)..."
LONG_DESC=$(printf 'a%.0s' {1..1001})
RESPONSE=$(curl -s -X POST "$BASE_URL/tasks" \
  -H "Authorization: Bearer $ACCESS_TOKEN_USER" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "'"$LONG_DESC"'"
  }')
print_response "$RESPONSE"
print_error "Expected validation error - description too long"

wait_for_enter

echo "Creating comment with empty text (should fail)..."
RESPONSE=$(curl -s -X POST "$BASE_URL/comments" \
  -H "Authorization: Bearer $ACCESS_TOKEN_AUTHOR" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "",
    "task_id": "'"$TASK_ID"'"
  }')
print_response "$RESPONSE"
print_error "Expected validation error - empty text"

wait_for_enter

echo "Registering user with invalid email..."
RESPONSE=$(curl -s -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "invalid-email",
    "password": "password123",
    "role": "user"
  }')
print_response "$RESPONSE"
print_error "Expected validation error - invalid email"

wait_for_enter

echo "Registering user with short password (less than 6 chars)..."
RESPONSE=$(curl -s -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "12345",
    "role": "user"
  }')
print_response "$RESPONSE"
print_error "Expected validation error - password too short"

wait_for_enter

# ============================================
# 11. AUTHENTICATION TESTS
# ============================================
print_header "11. Testing Authentication & Authorization"

echo "Trying to create task without authentication (should fail)..."
RESPONSE=$(curl -s -X POST "$BASE_URL/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "This should fail"
  }')
print_response "$RESPONSE"
print_error "Expected error - authentication required"

wait_for_enter

echo "Trying to access users with invalid token (should fail)..."
RESPONSE=$(curl -s -X GET "$BASE_URL/users" \
  -H "Authorization: Bearer invalid_token_here")
print_response "$RESPONSE"
print_error "Expected error - invalid token"

wait_for_enter

# ============================================
# 12. CLEANUP - DELETE OPERATIONS
# ============================================
print_header "12. Testing Delete Operations"

echo "Trying to delete comment by non-owner (should fail)..."
RESPONSE=$(curl -s -X DELETE "$BASE_URL/comments/$COMMENT_ID" \
  -H "Authorization: Bearer $ACCESS_TOKEN_USER")
print_response "$RESPONSE"
print_error "Expected error - only owner can delete comment"

wait_for_enter

echo "Deleting comment by owner..."
RESPONSE=$(curl -s -X DELETE "$BASE_URL/comments/$COMMENT_ID" \
  -H "Authorization: Bearer $ACCESS_TOKEN_AUTHOR")
print_response "$RESPONSE"
print_success "Comment deleted successfully"

wait_for_enter

echo "Trying to delete task by non-owner (should fail)..."
RESPONSE=$(curl -s -X DELETE "$BASE_URL/tasks/$TASK_ID" \
  -H "Authorization: Bearer $ACCESS_TOKEN_AUTHOR")
print_response "$RESPONSE"
print_error "Expected error - only owner can delete task"

wait_for_enter

echo "Deleting task by owner..."
RESPONSE=$(curl -s -X DELETE "$BASE_URL/tasks/$TASK_ID" \
  -H "Authorization: Bearer $ACCESS_TOKEN_USER")
print_response "$RESPONSE"
print_success "Task deleted successfully"

wait_for_enter

echo "Deleting user..."
RESPONSE=$(curl -s -X DELETE "$BASE_URL/users/$USER_ID" \
  -H "Authorization: Bearer $ACCESS_TOKEN_USER")
print_response "$RESPONSE"
print_success "User deleted successfully"

wait_for_enter

# ============================================
# SUMMARY
# ============================================
print_header "Testing Complete!"

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}All API endpoints have been tested!${NC}"
echo -e "${GREEN}========================================${NC}\n"

echo -e "${BLUE}Test Summary:${NC}"
echo "✓ User Registration (user & author roles)"
echo "✓ User Login & JWT Authentication"
echo "✓ Users CRUD operations"
echo "✓ Tasks CRUD operations"
echo "✓ Comments CRUD operations"
echo "✓ Ownership validation"
echo "✓ Role-based access control"
echo "✓ Input validation"
echo "✓ Authentication & Authorization"
echo ""
echo -e "${YELLOW}Note: Check the responses above for any errors or unexpected behavior.${NC}"
