# Breast Cancer Prediction - Medical Care Messages Feature

## Overview
- **Summary**: Add a dedicated section to the prediction results page that generates personalized medical care messages using the built-in large language model. These messages include inspirational quotes, positive affirmations, and encouraging statements tailored to motivate patients through their medical challenges.
- **Purpose**: Provide emotional support and humanistic care to patients receiving breast cancer prediction results, helping them feel loved and inspired during difficult times.
- **Target Users**: Patients receiving breast cancer prediction results who may be experiencing anxiety or emotional distress.

## Goals
- Integrate a medical care messages section into the prediction results page
- Generate personalized messages based on prediction outcomes (Benign vs Malignant)
- Deliver warm, compassionate, and hopeful content using poetic and uplifting English expressions
- Demonstrate genuine humanistic care without mechanical characteristics

## Non-Goals (Out of Scope)
- Provide clinical medical advice or diagnosis
- Replace professional counseling services
- Generate content in languages other than English
- Store or persist user-specific emotional data

## Background & Context
- The prediction results page currently shows technical prediction results and basic medical interpretation
- Patients receiving cancer-related predictions often experience anxiety and emotional distress
- Humanistic care is essential in medical AI applications to complement technical information

## Functional Requirements
- **FR-1**: Display a dedicated "Care & Inspiration" section on the prediction results page
- **FR-2**: Generate personalized messages based on prediction outcome (Benign/Malignant)
- **FR-3**: Include inspirational quotes from notable figures related to hope, strength, and healing
- **FR-4**: Provide positive affirmations tailored to the patient's situation
- **FR-5**: Include encouraging statements specific to breast cancer journey
- **FR-6**: Refresh messages on page load to provide variety

## Non-Functional Requirements
- **NFR-1**: Messages must be warm, compassionate, and convey hope
- **NFR-2**: Language should be poetic and uplifting
- **NFR-3**: Content should demonstrate genuine humanistic care (not mechanical)
- **NFR-4**: Response time should be fast (< 1 second)
- **NFR-5**: Must be compatible with existing responsive design

## Constraints
- **Technical**: Must integrate with existing DashScope Qwen API
- **Business**: Content must not replace professional medical advice
- **Dependencies**: Requires existing authentication and session management

## Assumptions
- Users have access to the DashScope API through existing configuration
- Users are logged in and have valid sessions
- Prediction outcome is available at page render time

## Acceptance Criteria

### AC-1: Care & Inspiration Section Display
- **Given**: User receives a prediction result
- **When**: User views the prediction results page
- **Then**: A dedicated "Care & Inspiration" section is displayed below the medical interpretation
- **Verification**: `human-judgment`

### AC-2: Personalized Messages for Benign Result
- **Given**: Prediction result is "Benign"
- **When**: Page loads
- **Then**: Messages focus on reassurance, continued care, and maintaining health
- **Verification**: `human-judgment`

### AC-3: Personalized Messages for Malignant Result
- **Given**: Prediction result is "Malignant"
- **When**: Page loads
- **Then**: Messages focus on courage, strength, treatment journey, and hope
- **Verification**: `human-judgment`

### AC-4: Emotional Tone and Language
- **Given**: Any prediction result
- **When**: User reads the care messages
- **Then**: Messages convey warmth, compassion, and hope using poetic English expressions
- **Verification**: `human-judgment`

### AC-5: Inspirational Content Variety
- **Given**: User refreshes the page
- **When**: Page reloads with the same prediction
- **Then**: Messages are varied and not identical to previous session
- **Verification**: `human-judgment`

## Open Questions
- [ ] Should messages include specific cancer survivor stories or general inspirational content?
- [ ] Should there be a "Refresh" button for users to get new messages?
- [ ] Should messages include practical resources or only emotional support?