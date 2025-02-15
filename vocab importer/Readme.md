# Vocabulary Generator

A modern web application that generates vocabulary lists in Spanish and Arabic with transliteration using AWS Bedrock and Claude 3 Sonnet AI model.

![Vocabulary Generator Screenshot](https://images.unsplash.com/photo-1546410531-bb4caa6b424d?auto=format&fit=crop&q=80&w=1200&h=600)

## Features

- 🌍 Multi-language support (Spanish and Arabic)
- 🤖 Powered by AWS Bedrock with Claude 3 Sonnet
- 📋 Easy copy-to-clipboard functionality
- 🎨 Modern, responsive UI using shadcn/ui
- ⚡ Built with Next.js 13+ App Router
- 🌙 Light/Dark mode support
- 🚀 Production-ready error handling

## Prerequisites

Before you begin, ensure you have:

- Node.js 18.x or later
- npm or yarn package manager
- AWS account with Bedrock access
- AWS credentials with appropriate permissions

## Environment Variables

Create a `.env.local` file in the root directory with the following variables:

```env
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
AWS_REGION=your_aws_region  # defaults to us-east-1
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd vocabulary-generator
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Usage

1. Enter a category in the input field (e.g., "Basic Greetings", "Food", "Colors")
2. Click "Generate Vocabulary" to create the vocabulary list
3. The generated JSON will appear in the text area below
4. Use the copy button to copy the JSON to your clipboard

Example output:
```json
{
  "group": {
    "name": "Basic Greetings"
  },
  "words": [
    {
      "spanish": "hola",
      "transliteration": "هولا",
      "arabic": "مرحبا"
    },
    {
      "spanish": "buenos días",
      "transliteration": "بوينوس دياس",
      "arabic": "صباح الخير"
    }
  ]
}
```

## Technology Stack

- **Framework**: Next.js 13+ with App Router
- **UI Components**: shadcn/ui
- **Styling**: Tailwind CSS
- **AI Model**: AWS Bedrock (Claude 3 Sonnet)
- **Icons**: Lucide React
- **State Management**: React Hooks
- **Notifications**: Toast notifications

## Project Structure

```
vocabulary-generator/
├── app/
│   ├── api/
│   │   └── generate/
│   │       └── route.ts    # AWS Bedrock API endpoint
│   ├── page.tsx            # Main application page
│   └── layout.tsx          # Root layout
├── components/
│   └── ui/                 # shadcn/ui components
├── hooks/
│   └── use-toast.ts        # Toast notification hook
└── public/
```

## Building for Production

To create a production build:

```bash
npm run build
```

To start the production server:

```bash
npm start
```

## AWS Bedrock Setup

1. Ensure you have access to AWS Bedrock in your AWS account
2. Create an IAM user with appropriate Bedrock permissions
3. Generate access keys for the IAM user
4. Add the credentials to your environment variables

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [AWS Bedrock](https://aws.amazon.com/bedrock/) for AI capabilities
- [shadcn/ui](https://ui.shadcn.com/) for the beautiful UI components
- [Next.js](https://nextjs.org/) for the amazing framework
- [Tailwind CSS](https://tailwindcss.com/) for styling