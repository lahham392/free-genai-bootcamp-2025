# GraphQL Schema Documentation

This document provides details about the GraphQL schema used in the Arabic MoM GraphQL Explorer.

## Types

### Meeting
```graphql
type Meeting {
  id: ID!
  meetingNumber: String!
  meetingTitle: String!
  meetingDate: String!
  meetingTime: String!
  meetingLocation: String!
  meetingChairman: String!
  createdAt: String
  pdfSource: String
  language: String!
  attendees: [Attendee]
  partialAttendees: [PartialAttendee]
  sections: [Section]
}
```

### Attendee
```graphql
type Attendee {
  id: ID!
  name: String!
  title: String
  role: String
  email: String
  meetings: [Meeting]
}
```

### PartialAttendee
```graphql
type PartialAttendee {
  id: ID!
  name: String!
  title: String
  role: String
  notes: String
}
```

### Section
```graphql
type Section {
  id: ID!
  title: String!
  order: Int!
  meetingId: ID!
  meeting: Meeting
  content: String
  subSections: [SubSection]
}
```

### SubSection
```graphql
type SubSection {
  id: ID!
  title: String!
  order: Int!
  sectionId: ID!
  section: Section
  content: String
  recommendations: [Recommendation]
  decisions: [Decision]
}
```

### Recommendation
```graphql
type Recommendation {
  id: ID!
  recommendationId: String!
  source: String!
  date: String
  content: String!
  subsectionId: ID
  subsection: SubSection
  relatedRecommendations: [Recommendation]
}
```

### Decision
```graphql
type Decision {
  id: ID!
  decisionId: String!
  date: String!
  content: String!
  subsectionId: ID
  subsection: SubSection
  basedOnRecommendations: [Recommendation]
  financialImpact: FinancialImpact
  actionItems: [ActionItem]
}
```

### FinancialImpact
```graphql
type FinancialImpact {
  id: ID!
  amount: Float!
  currency: String!
  description: String
  budgetSource: String
  decisionId: ID!
  decision: Decision
}
```

### ActionItem
```graphql
type ActionItem {
  id: ID!
  description: String!
  assignee: String!
  dueDate: String
  status: String!
  decisionId: ID!
  decision: Decision
}
```

## Queries

### Meetings
```graphql
# Get all meetings
query {
  meetings {
    id
    meetingNumber
    meetingTitle
    meetingDate
    meetingTime
    meetingLocation
    meetingChairman
    language
  }
}

# Get a specific meeting by ID
query {
  meeting(id: "m1") {
    id
    meetingTitle
    meetingDate
    # ... other fields
  }
}

# Get meetings by date range
query {
  meetingsByDate(startDate: "2023-01-01", endDate: "2023-12-31") {
    id
    meetingTitle
    meetingDate
  }
}
```

### Attendees
```graphql
# Get all attendees
query {
  attendees {
    id
    name
    title
    role
    email
  }
}

# Get a specific attendee by ID
query {
  attendee(id: "a1") {
    id
    name
    title
    role
    email
    meetings {
      id
      meetingTitle
    }
  }
}
```

### Sections and Subsections
```graphql
# Get sections by meeting
query {
  sectionsByMeeting(meetingId: "m1") {
    id
    title
    order
    content
  }
}

# Get subsections by section
query {
  subsectionsBySection(sectionId: "s1") {
    id
    title
    order
    content
  }
}
```

### Recommendations
```graphql
# Get recommendations by source
query {
  recommendationsBySource(source: "لجنة إدارة المخاطر") {
    id
    recommendationId
    source
    date
    content
    subsectionId
  }
}

# Get recommendations by subsection
query {
  recommendationsBySubsection(subsectionId: "ss1") {
    id
    recommendationId
    source
    date
    content
  }
}
```

### Decisions
```graphql
# Get decisions by meeting
query {
  decisionsByMeeting(meetingId: "m1") {
    id
    decisionId
    date
    content
    subsectionId
  }
}

# Get decisions by decision ID
query {
  decisionsByDecisionId(decisionId: "D001") {
    id
    decisionId
    date
    content
  }
}
```

### Action Items
```graphql
# Get action items by status
query {
  actionItemsByStatus(status: "pending") {
    id
    description
    assignee
    dueDate
    status
  }
}

# Get action items by assignee
query {
  actionItemsByAssignee(assignee: "Ahmed") {
    id
    description
    dueDate
    status
  }
}
```

## Important Notes

1. All query names use camelCase (e.g., `recommendationsBySource`, not `recommendations_by_source`)
2. All field names also use camelCase (e.g., `recommendationId`, not `recommendation_id`)
3. When filtering by IDs, make sure to use the correct ID format as defined in the sample data
