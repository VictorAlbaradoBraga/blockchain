import { Link } from "react-router-dom";

export default function Navbar({ onLogin, onLogout, isAuthenticated }) {
  return (
    <nav className="bg-white shadow-md">
      <div className="container mx-auto px-6 py-3 flex justify-between items-center">
        <div className="flex items-center space-x-6">
          <Link to="/" className="text-2xl font-bold text-blue-600 hover:text-blue-800">
            CertificaChain
          </Link>
          <Link to="/certificados" className="text-gray-600 hover:text-gray-800 font-medium">
            Certificados
          </Link>
          {isAuthenticated && (
            <>
              <Link to="/meus-certificados" className="text-gray-600 hover:text-gray-800 font-medium">
                Meus Certificados
              </Link>
              <Link to="/upload" className="text-gray-600 hover:text-gray-800 font-medium">
                Upload
              </Link>
            </>
          )}
        </div>
        <div>
          {isAuthenticated ? (
            <button
              onClick={onLogout}
              className="bg-red-500 hover:bg-red-600 text-white font-semibold px-4 py-2 rounded-md transition duration-300"
            >
              Logout
            </button>
          ) : (
            <button
              onClick={onLogin}
              className="bg-blue-500 hover:bg-blue-600 text-white font-semibold px-4 py-2 rounded-md transition duration-300"
            >
              Login
            </button>
          )}
        </div>
      </div>
    </nav>
  );
}
