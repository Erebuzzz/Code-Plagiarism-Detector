#!/bin/bash

echo "🚀 Replit Deployment Setup for AI Code Plagiarism Detector"
echo "=========================================================="

# Function to create .replit file
create_replit_config() {
    echo "📝 Creating .replit configuration..."
    cat > .replit << 'EOF'
run = "bash start.sh"
modules = ["python-3.10", "nodejs-18"]

[nix]
channel = "stable-22_11"

[env]
VIRTUAL_ENV = "/home/runner/${REPL_SLUG}/venv"
PATH = "${VIRTUAL_ENV}/bin"
PYTHONPATH = "$PYTHONHOME/lib/python3.10:${VIRTUAL_ENV}/lib/python3.10/site-packages"

[gitHubImport]
requiredFiles = [".replit", "replit.nix", "pyproject.toml"]

[deployment]
run = ["sh", "-c", "bash start.sh"]

[[ports]]
localPort = 5000
externalPort = 80

[languages]

[languages.python3]
pattern = "**/*.py"
[languages.python3.languageServer]
start = "pylsp"

[languages.javascript]
pattern = "**/{*.js,*.jsx,*.ts,*.tsx,*.json}"
[languages.javascript.languageServer]
start = "typescript-language-server --stdio"
EOF
    echo "✅ .replit file created"
}

# Function to create replit.nix file
create_nix_config() {
    echo "📝 Creating replit.nix configuration..."
    cat > replit.nix << 'EOF'
{ pkgs }: {
  deps = [
    pkgs.python310Full
    pkgs.nodejs-18_x
    pkgs.nodePackages.npm
    pkgs.nodePackages.typescript-language-server
    pkgs.replitPackages.prybar-python310
    pkgs.replitPackages.stderred
  ];
  env = {
    PYTHON_LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
      pkgs.stdenv.cc.cc.lib
      pkgs.zlib
      pkgs.glib
      pkgs.xorg.libX11
    ];
    PYTHONHOME = "${pkgs.python310Full}";
    PYTHONBIN = "${pkgs.python310Full}/bin/python3.10";
    LANG = "en_US.UTF-8";
    STDERREDBIN = "${pkgs.replitPackages.stderred}/bin/stderred";
    PRYBAR_PYTHON_BIN = "${pkgs.replitPackages.prybar-python310}/bin/prybar-python310";
  };
}
EOF
    echo "✅ replit.nix file created"
}

# Check if we're setting up for Replit
if [[ "$1" == "setup" ]]; then
    echo "🔧 Setting up Replit configuration files..."
    
    create_replit_config
    create_nix_config
    
    # Make start.sh executable
    chmod +x start.sh
    
    echo ""
    echo "🎉 Replit setup complete!"
    echo ""
    echo "📋 Next steps:"
    echo "1. Copy your .env file or set environment variables in Replit Secrets:"
    echo "   - COHERE_API_KEY"
    echo "   - TOGETHER_API_KEY" 
    echo "   - REPLICATE_API_TOKEN"
    echo ""
    echo "2. Push your code to GitHub (optional but recommended)"
    echo "3. Import your GitHub repo into Replit"
    echo "4. Click 'Run' in Replit"
    echo ""
    echo "🌐 Your app will be available at: https://your-repl-name.your-username.repl.co"
    
else
    echo "💡 Usage:"
    echo "  ./replit_setup.sh setup    # Create Replit configuration files"
    echo ""
    echo "📚 For detailed instructions, see REPLIT_DEPLOY.md"
fi
