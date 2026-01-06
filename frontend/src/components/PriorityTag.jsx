const PriorityTag = ({ priority }) => {
    const getColorClasses = () => {
        switch (priority?.toLowerCase()) {
            case 'high':
                return 'bg-red-100 text-red-700 border-red-300';
            case 'medium':
                return 'bg-yellow-100 text-yellow-700 border-yellow-300';
            case 'low':
                return 'bg-green-100 text-green-700 border-green-300';
            default:
                return 'bg-gray-100 text-gray-700 border-gray-300';
        }
    };

    if (!priority) {
        return <span className="px-3 py-1 rounded-full text-xs font-semibold bg-gray-100 text-gray-500 border border-gray-300">N/A</span>;
    }

    return (
        <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${getColorClasses()}`}>
            {priority.toUpperCase()}
        </span>
    );
};

export default PriorityTag;
