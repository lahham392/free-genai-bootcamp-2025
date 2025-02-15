# Language Portal

A modern web application for learning languages through interactive study activities, with a focus on Spanish-Arabic translations.

![Language Portal Screenshot](https://images.unsplash.com/photo-1546521343-4eb2c01aa44b?w=800&auto=format&fit=crop&q=60)

## Features

- 📚 Multiple study activities (flashcards, word matching, sentence building)
- 👥 Word group management for organized learning
- 📊 Detailed progress tracking and statistics
- 📱 Responsive design for all devices
- 🌙 Light/dark mode support
- 📈 Study session history and performance analytics

## Tech Stack

- **Frontend Framework**: React with TypeScript
- **Routing**: React Router v6
- **State Management**: React Query
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui
- **Icons**: Lucide React
- **Date Handling**: date-fns
- **Build Tool**: Vite

## Getting Started

### Prerequisites

- Node.js 18 or higher
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/language-portal.git
cd language-portal
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Project Structure

```
src/
├── components/        # Reusable UI components
│   ├── ui/           # shadcn/ui components
│   └── layout.tsx    # Main layout component
├── hooks/            # Custom React hooks
├── lib/              # Utilities and API functions
├── pages/            # Page components
└── types/            # TypeScript type definitions
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Features in Detail

### Study Activities

- **Vocabulary Flashcards**: Practice words with digital flashcards
- **Word Match Game**: Match words between languages
- **Sentence Builder**: Create sentences by arranging words

### Word Groups

- Create and manage word collections
- Track progress per group
- View detailed statistics

### Progress Tracking

- Success rate monitoring
- Study streak tracking
- Detailed session history
- Performance analytics

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [shadcn/ui](https://ui.shadcn.com/) for the beautiful UI components
- [Tailwind CSS](https://tailwindcss.com/) for the utility-first CSS framework
- [Lucide](https://lucide.dev/) for the icon set
- [Unsplash](https://unsplash.com/) for the images